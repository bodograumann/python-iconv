import sys, iconv, codecs, errno

# First we need to find out what the Unicode code set name is
# in this iconv implementation

if sys.platform.startswith("linux"):
    unicodename = "unicode"+sys.byteorder
else:
    # may need to try UCS-2, UCS-2-LE/BE, Unicode, ...
    raise ImportError,"cannot establish name of 2-byte Unicode"

class Codec(codecs.Codec):
    def __init__(self):
        self.encoder = iconv.open(self.codeset,unicodename)
        self.decoder = iconv.open(unicodename,self.codeset)
        
    def encode(self, msg, errors = 'strict'):
        try:
            return self.encoder.iconv(msg),len(msg)
        except iconv.error,e:
            print e
            errstring,code,inlen,outres=e.args
            assert inlen % 2 == 0
            inlen /= 2
            if code == errno.E2BIG:
                # outbuffer was too small, try to encode rest
                out1,len1 = self.encode(msg[inlen:],errors)
                return outres+out1, inlen+len1
            if code == errno.EINVAL:
                # An incomplete multibyte sequence has been
                # encountered in the input. Should not happen in Unicode
                raise AssertionError("EINVAL in encode")
            if code == errno.EILSEQ:
                # An invalid multibyte sequence has been encountered
                # in the input. Used to indicate that the character is
                # not supported in the target code
                if errors == 'strict':
                    raise UnicodeError(*args)
                if errors == 'replace':
                    out1,len1 = self.encode(u"?"+msg[inlen+1:],errors)
                elif errors == 'ignore':
                    out1,len1 = self.encode(msg[inlen+1:],errors)
                else:
                    raise ValueError("unsupported error handling")
                return outres+out1, inlen+1+len1
            raise

    def decode(self, msg, errors = 'strict'):
        try:
            return self.decoder.iconv(msg, return_unicode=1),len(msg)
        except iconv.error,e:
            errstring,code,inlen,outres = e.args
            if code == errno.E2BIG:
                # buffer too small
                out1,len1 = self.decode(msg[inlen:],errors)
                return outres+out1, inlen+len1
            if code == errno.EINVAL:
                # An incomplete multibyte sequence has been
                # encountered in the input.
                return outres,inlen
            if code == errno.EILSEQ:
                # An invalid multibyte sequence has been encountered
                # in the input. Ignoring or replacing it is hard to
                # achieve, just try one character at a time
                if errors == 'strict':
                    raise UnicodeError(*e.args)
                if errors == 'replace':
                    outres += u'\uFFFD'
                    out1,len1 = self.decode(msg[inlen:],errors)
                elif errors == 'ignore':
                    out1,len1 = self.decode(msg[inlen:],errors)
                else:
                    raise ValueError("unsupported error handling")
                return outres+out1,inlen+len1

def lookup(encoding):
    class SpecialCodec(Codec):pass
    SpecialCodec.codeset = encoding
    class Reader(SpecialCodec, codecs.StreamReader):pass
    class Writer(SpecialCodec, codecs.StreamWriter):pass
    try:
        return SpecialCodec().encode,SpecialCodec().decode, Reader, Writer
    except ValueError:
        return None

codecs.register(lookup)
