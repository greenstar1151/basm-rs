# read prestub
with open("static-pie-prestub-amd64.bin", "rb") as f:
    prestub = f.read()
prestub = bytearray(prestub)
if len(prestub) > 0 and prestub[-1] == 0:
    prestub = prestub[:-1]
    asciz = True
else:
    asciz = False

# special handling for trailing ASCII characters
j = len(prestub)
b85_table = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~"
while j > 0 and prestub[j-1] in b85_table:
    j -= 1
while j < len(prestub) and j % 8 != 0:
    j += 1
table_part = prestub[j:]
prestub = prestub[:j]

# pad to align at 8-byte boundary
while len(prestub) % 8 != 0:
    prestub.append(0)

# convert each 8-byte chunk
out = []
for i in range(0, len(prestub), 8):
    if i == 0:
        out.append("        \".quad ")
    elif i % 32 == 0:
        out.append("        ")
    x = int.from_bytes(prestub[i:i+8], "little")
    def to_hex_short(y):
        out = str(hex(y))[2:]
        nonzero_idx = len(out)
        while nonzero_idx > 1 and out[nonzero_idx-1] == '0':
            nonzero_idx -= 1
        out2 = out[:nonzero_idx] + "h<<" + str((len(out) - nonzero_idx) * 4)
        out = out + "h"
        if len(out2) < len(out):
            print(out2, out)
            out = out2
        if ord(out[0]) >= ord('a'):
            out = "0" + out
        return out
    qword1 = to_hex_short(x)
    qword2 = str(x)
    if len(qword1) <= len(qword2):
        out.append(qword1)
    else:
        out.append(qword2)
    if i + 8 == len(prestub):
        out.append("\",\n")
    elif i % 32 == 24:
        out.append(",\\\n")
    else:
        out.append(",")

# convert the table part
table_part = table_part.decode('ascii')
table_part = table_part.replace('{', '{{').replace('}', '}}').replace('$', '\\\\x24')
out.append("        \"{0} \\\"{1}\\\"\",\n".format(".asciz" if asciz else ".ascii", table_part))

# print the result
print("".join(out))