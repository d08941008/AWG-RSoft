import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
def str2(var):
    return var if isinstance(var, str) else str(var)

def writeSegment(indFName, i, begin_x = None, begin_y = None, begin_z = None, end_x = None, end_y = None, end_z = None, 
                                orientation = 1, draw_priority = 2, cld = 0, begin_height = None, end_height = None, 
                                width_taper = None, position_taper = 0, color = 12, mask_layer = 7100, 
                                begin_width = None, end_width = None, profile_type = 1, 
                                arc_type = None, arc_radius = None, arc_iangle = None, arc_fangle = None):
    position_taperStr = [0, 'TAPER_LINEAR', 'TAPER_ARC']
    segmentStr = [
        'segment ' + str(i), 
        '   profile_type = PROF_INACTIVE' if profile_type == 0 else '', 
        '   draw_priority = ' + str(draw_priority), 
        '   mask_layer = ' + str(mask_layer), 
        '   color = ' + str2(color), 
        '   orientation = ' + str(orientation), 
        '   width_taper = ' + str2(width_taper) if width_taper != None else '', 
        '   position_taper = ' + position_taperStr[position_taper] if position_taper !=0 else '', 
        '   begin.x = ' + str2(begin_x) if begin_x != None else '', 
        '   begin.y = ' + str2(begin_y) if begin_y != None else '', 
        '   begin.z = ' + str2(begin_z) if begin_z != None else '', 
        '   begin.width = ' + str2(begin_width) if begin_width != None else '', 
        '   begin.height = ' + str2(begin_height) if begin_height != None else '', 
        '   end.width = ' + str2(end_width) if end_width != None else '', 
        '   arc_type = ' + str2(arc_type) if arc_type != None else '', 
        '   arc_radius = ' + str2(arc_radius) if arc_radius != None else '', 
        '   arc_iangle = ' + str2(arc_iangle) if arc_iangle != None else '', 
        '   arc_fangle = ' + str2(arc_fangle) if arc_fangle != None else '', 
        '   end.x = ' + str2(end_x) if end_x != None else '', 
        '   end.y = ' + str2(end_y) if end_y != None else '', 
        '   end.z = ' + str2(end_z) if end_z != None else '', 
        '   end.height = ' + str2(end_height) if end_height != None else '', 
    ]
    segmentStr = [x for x in segmentStr if x]
    segmentStr.append('end segment')
    with open(indFName, 'a') as foh:
        foh.write('\n'.join(segmentStr))
        foh.write('\n\n')
    return i+1
##..................................................................
idxSeg = 37
for i in range(16):
    idxSeg = writeSegment(indFName = 'in.txt', i = idxSeg, 
                        orientation = 1, color = 14, mask_layer = 0, 
                        width_taper = 'width_taper_out', position_taper = 1, 
                        begin_x = '(Ro-Lom)*sin(zAa'+str(i+1)+') rel begin segment 2', 
                        begin_z = 'S*(Ro-Lom)*cos(zAa'+str(i+1)+') rel begin segment 2', 
                        begin_width = 'Wom*2', begin_height = 'height2', end_height = 'height2', 
                        end_x = '(RLots)*sin(zAa'+str(i+1)+') rel begin segment 2', 
                        end_z = 'S*(RLots)*cos(zAa'+str(i+1)+') rel begin segment 2', 
                        draw_priority = -1, cld = 0, 
                        )

for i in range(1):
    idxSeg = writeSegment(indFName = 'in.txt', i = idxSeg, 
                        orientation = 1, color = 14, mask_layer = 0, 
                        width_taper = 'width_taper_out', position_taper = 1, 
                        begin_x = '(Ri-Lim)*sin(zAi'+str(i+1)+') rel end segment 2', 
                        begin_z = 'S*(Ri-Lim)*cos(zAi'+str(i+1)+') rel end segment 2', 
                        begin_width = 'Wim*2', begin_height = 'height2', end_height = 'height2', 
                        end_x = '(Ri+Lots)*sin(zAi'+str(i+1)+') rel end segment 2', 
                        end_z = 'S*(Ri+Lots)*cos(zAi'+str(i+1)+') rel end segment 2', 
                        draw_priority = -1, cld = 0, 
                        )
idxSeg = writeSegment(indFName = 'in.txt', i = idxSeg, 
                        orientation = 1, color = 14, mask_layer = 0, position_taper = 2, 
                        begin_x = '(Ro+Lotss/2)*sin(zAa16) rel begin segment 2', 
                        begin_z = 'S*(Ro+Lotss/2)*cos(zAa16) rel begin segment 2', 
                        begin_width = 'Lotss', end_width = 'Lotss', 
                        begin_height = 'height2', end_height = 'height2', 
                        arc_type = 'ARC_FREE', arc_radius = 'Ro+Lotss/2', 
                        arc_iangle = '-90+zAa16', arc_fangle = '-90+zAa1', 
                        draw_priority = -1, cld = 0, 
                        )
