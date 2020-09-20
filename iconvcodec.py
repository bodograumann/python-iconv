import sys, iconv, codecs, errno

def codec_factory(encoding):
    encoder = iconv.open(encoding, "utf-8")
    decoder = iconv.open("utf-8", encoding)

    def encode(input, errors="strict"):
        msg = input.encode()
        try:
            return encoder.iconv(msg), len(msg)
        except iconv.error as e:
            errstring, code, inlen, outres = e.args
            assert inlen % 2 == 0
            inlen /= 2
            if code == errno.E2BIG:
                # outbuffer was too small, try to encode rest
                out1, len1 = encode(msg[inlen:], errors)
                return outres + out1, inlen + len1
            if code == errno.EINVAL:
                # An incomplete multibyte sequence has been
                # encountered in the input. Should not happen in Unicode
                raise AssertionError("EINVAL in encode")
            if code == errno.EILSEQ:
                # An invalid multibyte sequence has been encountered
                # in the input. Used to indicate that the character is
                # not supported in the target code
                if errors == "strict":
                    raise UnicodeError(*e.args)
                if errors == "replace":
                    out1, len1 = encode(u"?" + msg[inlen + 1 :], errors)
                elif errors == "ignore":
                    out1, len1 = encode(msg[inlen + 1 :], errors)
                else:
                    raise ValueError("unsupported error handling")
                return outres + out1, inlen + 1 + len1
            raise

    def decode(msg, errors="strict"):
        try:
            return decoder.iconv(msg).decode(), len(msg)
        except iconv.error as e:
            errstring, code, inlen, outres = e.args
            if code == errno.E2BIG:
                # buffer too small
                out1, len1 = decode(msg[inlen:], errors)
                return outres.decode() + out1, inlen + len1
            if code == errno.EINVAL:
                # An incomplete multibyte sequence has been
                # encountered in the input.
                return outres.decode(), inlen
            if code == errno.EILSEQ:
                # An invalid multibyte sequence has been encountered
                # in the input. Ignoring or replacing it is hard to
                # achieve, just try one character at a time
                if errors == "strict":
                    raise UnicodeError(*e.args)
                if errors == "replace":
                    outres += u"\uFFFD"
                    out1, len1 = decode(msg[inlen:], errors)
                elif errors == "ignore":
                    out1, len1 = decode(msg[inlen:], errors)
                else:
                    raise ValueError("unsupported error handling")
                return outres.decode() + out1, inlen + len1

    return encode, decode


def lookup(encoding):
    try:
        encode, decode = codec_factory(encoding)
    except ValueError:
        # Encoding not supported by iconv
        return None

    class StreamWriter(codecs.StreamWriter):
        nonlocal encode

    class StreamReader(codecs.StreamReader):
        nonlocal decode

    class IncrementalEncoder(codecs.IncrementalEncoder):
        def encode(self, input, final=False):
            nonlocal encode
            return encode(input, self.errors)[0]

    class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
        def _buffer_decode(self, input, errors, final):
            nonlocal decode
            return decode(input, errors)

    return codecs.CodecInfo(
        name=encoding,
        encode=encode,
        decode=decode,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
    )


codecs.register(lookup)
