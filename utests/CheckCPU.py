def checkCPU(t, c, ptr, ax, bx, cx, dx, stack_ptr, stack):
    t.assertEqual(c.ptr, ptr)
    t.assertEqual(c.ax, ax)
    t.assertEqual(c.bx, bx)
    t.assertEqual(c.cx, cx)
    t.assertEqual(c.dx, dx)
    t.assertEqual(c.stack_ptr, stack_ptr)
    t.assertEqual(c.stack, stack)