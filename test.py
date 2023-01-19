def test(a, b, *args, **kwargs):
    print(a, b)

test(10, 20, 30, 40, 50, pk=123, asdf=1234, zxcv=123)
