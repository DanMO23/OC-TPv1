2000:
lw x1, 1000(x2)
sw x1, 1000(x2)
add x2, x0, x1
sll X1, x2, x2
xor x4, x2, x3
addi x3, x2, -243
bne x10, x11, 2000
