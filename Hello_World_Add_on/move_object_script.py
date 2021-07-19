# -*- coding: utf-8 -*-

import bpy

scene = bpy.context.scene
for obj in scene.objects:
	obj.location.x += 1.0
	obj.location.y += 2.0