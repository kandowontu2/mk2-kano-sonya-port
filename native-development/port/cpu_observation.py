"""Conservative attract-trace filtering; post-fill is not a gameplay proof."""
def post_health_fill_observations(observations,actor):
    accepted=[];previous_context=None;previous_frame=None;armed=False;full_frames=[]
    for row,side in observations:
        frame=int(row['frame'])
        context=(side,row['p1char'],row['p2char'],row['p1selected'],row['p2selected'])
        if context!=previous_context or previous_frame is None or frame!=previous_frame+2:
            armed=False
        if not armed and row['p1hp']==row['p2hp']=='161':
            armed=True;full_frames.append(frame)
        previous_context=context;previous_frame=frame
        if armed and frame>3000 and int(row[f'p{side}selected'])==actor and all(
                0<int(row[f'p{s}hp'])<=161 and 0<=int(row[f'p{s}char'])<=18 for s in (1,2)):
            accepted.append((row,side))
    return accepted,full_frames
