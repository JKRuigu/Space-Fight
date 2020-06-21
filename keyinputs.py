if event.type == pygame.KEYDOWN:
	if event.key == pygame.K_LEFT:
		player.move(-1)
	if event.key == pygame.K_RIGHT:
		player.move(1)
if event.type == pygame.KEYUP:
	if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
		player.move(0)