import iconv

s=iconv.open("utf-8","latin1")
r=s.iconv(b"Hallo")
print(repr(r),len(r))

s=iconv.open("utf-8","utf-16")
r=s.iconv(b"Hallo", 10)
print(repr(r),len(r))

s=iconv.open("unicodelittle","iso-8859-1")
r=s.iconv(b"Hallo",11,return_unicode=1)
print(repr(r),len(r))

s=iconv.open("iso-8859-1","unicodelittle")
r=s.iconv("Hallo",110)
print(r)
