havoc x, y;
assume y = 4;
c := 0;
r := x;
while c < y
inv r = x - c and c <= y
do
{
  r := r - 1;
  c := c + 1
};
assert r = x - y