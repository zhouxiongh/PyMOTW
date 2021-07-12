import array
import binascii
import tempfile

a = array.array('i', range(5))
print('A1:', a)

output = tempfile.NamedTemporaryFile()
a.tofile(output.file)
output.flush()

with open(output.name, 'rb') as input:
    raw_data = input.read()
    print('Raw Contents:', binascii.hexlify(raw_data))

    # Read the data into an array
    input.seek(0)
    a2 = array.array('i')
    a2.fromfile(input, len(a))
    print('A2:', a2)
