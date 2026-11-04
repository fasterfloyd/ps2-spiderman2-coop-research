.set noreorder
.set noat
.set mips3
.text
.globl spawn_dispatch
.ent spawn_dispatch
spawn_dispatch:
    addiu   $sp,$sp,-0x80
    sd      $ra,0x70($sp)
    sd      $s0,0x68($sp)
    sd      $s1,0x60($sp)
    lui     $s0,0x000f
    ori     $s0,$s0,0xf100
    lw      $t0,0x14($s0)       # one-shot spawn request
    beq     $t0,$zero,done
    nop
    sw      $zero,0x14($s0)
    addiu   $t1,$zero,1
    sw      $t1,0x1c($s0)       # stage 1: request seen
    sw      $zero,0x18($s0)     # clear result pointer
    lui     $s1,0x00b3
    ori     $s1,$s1,0x05a0     # validated P1 object in prior states
    lw      $t0,0x10($s1)
    lui     $t1,0x0064
    ori     $t1,$t1,0x6d20
    bne     $t0,$t1,bad_hero
    nop
    lw      $t0,0x14($s1)
    addiu   $t1,$zero,0x39
    bne     $t0,$t1,bad_hero
    nop
    lw      $a1,0($s1)         # hero entity identifier POINTER (reuse is experimental)
    beq     $a1,$zero,bad_hero
    nop
    lui     $a0,0x000f
    ori     $a0,$a0,0xda00    # &class_name_ptr (points at "SPIDERMANX")
    addiu   $t1,$zero,2
    sw      $t1,0x1c($s0)     # stage 2: about to call factory
    jal     0x004cc080        # real game class factory
    nop
    sw      $v0,0x18($s0)     # pointer returned
    beq     $v0,$zero,no_object
    nop
    addiu   $t1,$zero,3
    sw      $t1,0x1c($s0)     # stage 3: pointer returned (not proof of render)
    b       done
    nop
bad_hero:
    addiu   $t1,$zero,-2
    sw      $t1,0x1c($s0)
    b       done
    nop
no_object:
    addiu   $t1,$zero,-3
    sw      $t1,0x1c($s0)
done:
    ld      $s1,0x60($sp)
    ld      $s0,0x68($sp)
    ld      $ra,0x70($sp)
    jr      $ra
    addiu   $sp,$sp,0x80
.end spawn_dispatch
