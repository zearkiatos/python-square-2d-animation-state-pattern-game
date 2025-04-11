from typing import Callable
import pygame
import esper

from src.ecs.components.c_input_command import CInputCommand, CommandPhase
# from src.utils.sounds import generate_laser_beep

def system_input_player(world: esper.World, event: pygame.event.Event, do_action:Callable[[CInputCommand, pygame.event.Event], None]):
    components = world.get_component(CInputCommand)

    for _,c_input in components:
        if event.type == pygame.KEYDOWN and c_input.key == event.key:
            c_input.phase = CommandPhase.START
            do_action(c_input, None)
        elif event.type == pygame.KEYUP and c_input.key == event.key:
            c_input.phase = CommandPhase.END
            do_action(c_input, None)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # laser_sound = generate_laser_beep()
            # laser_sound.play()
            c_input.phase = CommandPhase.START
            do_action(c_input, event)
        elif event.type == pygame.MOUSEBUTTONUP:
            c_input.phase = CommandPhase.END
            do_action(c_input, event)