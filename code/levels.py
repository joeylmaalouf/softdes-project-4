from base import Level


level1 = Level()
level1.add_piece(128, 12, 8, 400)
level1.add_piece(64, 10, 180, 480)
level1.add_piece(80, 8, 300, 550)
level1.add_enemy(24, 24, 430, 8, 0, 1)
level1.add_enemy(24, 24, 430, 360, 0, 1)
level1.add_piece(80, 12, 500, 500)
level1.add_piece(96, 16, 640, 600)
level1.add_piece(64, 16, 800, 560)
level1.add_enemy(32, 32, 900, 8, 0, -1.5)
level1.add_enemy(32, 32, 900, 360, 0, -1.5)
level1.add_goal(64, 64, 1000, 500)

level2 = Level()
level2.add_piece(1280, 4, 0, 716)
level2.add_piece(64, 10, 300, 600)
level2.add_piece(64, 10, 200, 490)
level2.add_piece(64, 10, 390, 380)
level2.add_piece(64, 10, 600, 380)
level2.add_enemy(384, 384, 400, 400, 0, 0)
level2.add_goal(64, 64, 1000, 500)
