# GATE-LOG.md — gistgap-pitch

Console output of the review builds (`./art run <reel> --height 2160`, strict
gates: ART_STRICT=1, facts gate on, no overrides), each followed by `./art todo`,
and of the final export attempts (`./art final <reel> --height 2160`, same
settings).
Absolute home-folder paths were replaced with `<home>`; nothing else was edited (Manim's progress-bar carriage returns are kept as printed).
`layout_audit.md` holds only the last rendered scene's Gate B audit, because the toolkit overwrites it for each scene; the per-scene Gate A, W and B results are in these logs.
Earlier runs (run 2 and run 3) are superseded and not included.

## gistgap-run4.log

Run 4 — full rebuild (2026-10-10): B01–B12 re-rendered from the new scenes.py after moving their old clips to _superseded/; B13 and the B14 card reused.

```text
### ./art run <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film --height 2160
[run] skip B13_Columns — B13 already filled
[run] GATE L — beat-mix lint
[beat-lint] clean — beat mix OK (beat_sheet.json)
[run] GATE SHAPE — finance chart-shape enforcement
[gate-shape] skip — not a finance reel (beat_sheet.json)
[run] GATE A — static pre-flight

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[run] GATE W — WCAG contrast + margins + text-overlap (independent second check)
[gateW] B01_Agent clean
[gateW] B02_ShownSigned clean
[gateW] B03_Contract clean
[gateW] B04_Browser clean
[gateW] B05_Checklist clean
[gateW] B06_Landscape clean
[gateW] B07_Examples clean
[gateW] B08_Skills clean
[gateW] B09_Fields clean
[gateW] B10_ScopeTest clean
[gateW] B11_Shrink clean
[gateW] B12_GitLog clean
[run] rendering B01_Agent
Manim Community v0.18.1


Animation 0: FadeIn(VGroup of 9 submobjects):   0%|          | 0/17 [00:00<?, ?it/s]
Animation 0: FadeIn(VGroup of 9 submobjects):  53%|█████▎    | 9/17 [00:00<00:00, 88.77it/s]
                                                                                            
[10/10/26 20:35:38] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B01_Agent/342                         
                             9491395_723264930_42020405                         
                             26.mp4'                                            
[10/10/26 20:35:39] INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B01_Agent/160                         
                             6801221_482066956_17644195                         
                             96.mp4'                                            

Animation 2: FadeIn(VGroup of 4 submobjects):   0%|          | 0/12 [00:00<?, ?it/s]
Animation 2: FadeIn(VGroup of 4 submobjects):  83%|████████▎ | 10/12 [00:00<00:00, 95.17it/s]
                                                                                             
                    INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B01_Agent/160                         
                             6801221_1003747375_1099055                         
                             280.mp4'                                           
                    INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B01_Agent/160                         
                             6801221_2762319436_1459240                         
                             019.mp4'                                           
[10/10/26 20:35:40] INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B01_Agent/160                         
                             6801221_161148042_40988358                         
                             79.mp4'                                            

Animation 5: FadeIn(Polygon):   0%|          | 0/10 [00:00<?, ?it/s]
                                                                    
                    INFO     Animation 5 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B01_Agent/160                         
                             6801221_3534095609_2398475                         
                             988.mp4'                                           
                    INFO     Animation 6 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B01_Agent/160                         
                             6801221_751031276_39210859                         
                             78.mp4'                                            

Animation 7: FadeIn(Text('?')):   0%|          | 0/10 [00:00<?, ?it/s]
                                                                      
                    INFO     Animation 7 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B01_Agent/160                         
                             6801221_1463294999_3278900                         
                             396.mp4'                                           
[10/10/26 20:35:41] INFO     Animation 8 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B01_Agent/160                         
                             6801221_3581043413_2065352                         
                             969.mp4'                                           
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B01_Age                         
                             nt.mp4'                                            
                                                                                
                    INFO     Rendered B01_Agent                     scene.py:247
                             Played 9 animations                                
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim

Animation 0: FadeIn(VGroup of 9 submobjects):   0%|          | 0/11 [00:00<?, ?it/s]
                                                                                    
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 2: FadeIn(VGroup of 4 submobjects):   0%|          | 0/8 [00:00<?, ?it/s]
                                                                                   

Animation 5: FadeIn(Polygon):   0%|          | 0/6 [00:00<?, ?it/s]
                                                                   

Animation 7: FadeIn(Text('?')):   0%|          | 0/6 [00:00<?, ?it/s]
                                                                     
[audit] scenes: 14 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[run] rendering B02_ShownSigned
Manim Community v0.18.1

[10/10/26 20:35:42] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B02_ShownSign                         
                             ed/3429491395_1087462861_1                         
                             62172165.mp4'                                      

Animation 1: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/15 [00:00<?, ?it/s]
Animation 1: FadeIn(VGroup of 3 submobjects), etc.:  67%|██████▋   | 10/15 [00:00<00:00, 94.58it/s]
                                                                                                   
[10/10/26 20:35:43] INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B02_ShownSign                         
                             ed/1606801221_3561442011_2                         
                             333425766.mp4'                                     
[10/10/26 20:35:44] INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B02_ShownSign                         
                             ed/1606801221_2413939939_2                         
                             147031448.mp4'                                     
                    INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B02_ShownSign                         
                             ed/1606801221_1337691166_6                         
                             74567195.mp4'                                      

Animation 4: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/15 [00:00<?, ?it/s]
Animation 4: FadeIn(VGroup of 2 submobjects), etc.:  67%|██████▋   | 10/15 [00:00<00:00, 95.41it/s]
                                                                                                   
                    INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B02_ShownSign                         
                             ed/1606801221_2635560133_2                         
                             308284097.mp4'                                     
[10/10/26 20:35:45] INFO     Animation 5 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B02_ShownSign                         
                             ed/1606801221_1539995130_4                         
                             022932046.mp4'                                     
                    INFO     Animation 6 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B02_ShownSign                         
                             ed/1606801221_3778742912_1                         
                             014255438.mp4'                                     

Animation 7: FadeIn(Text('?')):   0%|          | 0/10 [00:00<?, ?it/s]
                                                                      
                    INFO     Animation 7 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B02_ShownSign                         
                             ed/1606801221_565446995_12                         
                             11786117.mp4'                                      
[10/10/26 20:35:46] INFO     Animation 8 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B02_ShownSign                         
                             ed/1606801221_968811856_26                         
                             82847276.mp4'                                      
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B02_Sho                         
                             wnSigned.mp4'                                      
                                                                                
                    INFO     Rendered B02_ShownSigned               scene.py:247
                             Played 9 animations                                
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 1: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/9 [00:00<?, ?it/s]
                                                                                         

Animation 4: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/9 [00:00<?, ?it/s]
                                                                                         

Animation 7: FadeIn(Text('?')):   0%|          | 0/6 [00:00<?, ?it/s]
                                                                     
[audit] scenes: 15 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[run] rendering B03_Contract
Manim Community v0.18.1


Animation 0: FadeIn(VGroup of 5 submobjects):   0%|          | 0/12 [00:00<?, ?it/s]
Animation 0: FadeIn(VGroup of 5 submobjects):  67%|██████▋   | 8/12 [00:00<00:00, 73.41it/s]
                                                                                            
[10/10/26 20:35:47] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B03_Contract/                         
                             3429491395_1297818944_3124                         
                             034031.mp4'                                        
[10/10/26 20:35:48] INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B03_Contract/                         
                             1606801221_2025129696_5047                         
                             93344.mp4'                                         

Animation 2: FadeIn(Text('cover: $50')):   0%|          | 0/10 [00:00<?, ?it/s]
Animation 2: FadeIn(Text('cover: $50')): 100%|██████████| 10/10 [00:00<00:00, 96.48it/s]
                                                                                        
                    INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B03_Contract/                         
                             1606801221_1332577595_5979                         
                             38649.mp4'                                         
[10/10/26 20:35:49] INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B03_Contract/                         
                             1606801221_3148553097_3533                         
                             538428.mp4'                                        

Animation 4: MoveAlongPath(VGroup of 3 submobjects):   0%|          | 0/15 [00:00<?, ?it/s]
Animation 4: MoveAlongPath(VGroup of 3 submobjects):  73%|███████▎  | 11/15 [00:00<00:00, 101.40it/s]
                                                                                                     
                    INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B03_Contract/                         
                             1606801221_1550827663_4521                         
                             13197.mp4'                                         
                    INFO     Animation 5 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B03_Contract/                         
                             1606801221_2764074932_2203                         
                             647266.mp4'                                        

Animation 6: FadeIn(Line):   0%|          | 0/5 [00:00<?, ?it/s]
                                                                
[10/10/26 20:35:50] INFO     Animation 6 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B03_Contract/                         
                             1606801221_1166566102_2015                         
                             6978.mp4'                                          

Animation 7: _MethodAnimation(Line):   0%|          | 0/15 [00:00<?, ?it/s]
Animation 7: _MethodAnimation(Line):  80%|████████  | 12/15 [00:00<00:00, 116.08it/s]
                                                                                     
                    INFO     Animation 7 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B03_Contract/                         
                             1606801221_2875465372_1903                         
                             801973.mp4'                                        

Animation 8: FadeOut(Line), etc.:   0%|          | 0/8 [00:00<?, ?it/s]
                                                                       
                    INFO     Animation 8 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B03_Contract/                         
                             1606801221_2468293820_1903                         
                             801973.mp4'                                        

Animation 9: Create(ArcBetweenPoints):   0%|          | 0/20 [00:00<?, ?it/s]
Animation 9: Create(ArcBetweenPoints):  55%|█████▌    | 11/20 [00:00<00:00, 105.33it/s]
                                                                                       
[10/10/26 20:35:51] INFO     Animation 9 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B03_Contract/                         
                             1606801221_2629466986_4194                         
                             145511.mp4'                                        

Animation 10: FadeIn(Dot):   0%|          | 0/8 [00:00<?, ?it/s]
                                                                
                    INFO     Animation 10 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B03_Contract/                         
                             1606801221_61357637_136599                         
                             3621.mp4'                                          
[10/10/26 20:35:52] INFO     Animation 11 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B03_Contract/                         
                             1606801221_591285248_42102                         
                             5861.mp4'                                          
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B03_Con                         
                             tract.mp4'                                         
                                                                                
                    INFO     Rendered B03_Contract                  scene.py:247
                             Played 12 animations                               
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim

Animation 0: FadeIn(VGroup of 5 submobjects):   0%|          | 0/8 [00:00<?, ?it/s]
                                                                                   
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 2: FadeIn(Text('cover: $50')):   0%|          | 0/6 [00:00<?, ?it/s]
                                                                              

Animation 4: MoveAlongPath(VGroup of 3 submobjects):   0%|          | 0/11 [00:00<?, ?it/s]
                                                                                           

Animation 6: FadeIn(Line):   0%|          | 0/3 [00:00<?, ?it/s]
                                                                

Animation 7: _MethodAnimation(Line):   0%|          | 0/9 [00:00<?, ?it/s]
                                                                          

Animation 8: FadeOut(Line), etc.:   0%|          | 0/5 [00:00<?, ?it/s]
                                                                       

Animation 9: Create(ArcBetweenPoints):   0%|          | 0/12 [00:00<?, ?it/s]
                                                                             

Animation 10: FadeIn(Dot):   0%|          | 0/5 [00:00<?, ?it/s]
                                                                
[audit] scenes: 16 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[run] rendering B04_Browser
Manim Community v0.18.1


Animation 0: FadeIn(VGroup of 5 submobjects), etc.:   0%|          | 0/15 [00:00<?, ?it/s]
Animation 0: FadeIn(VGroup of 5 submobjects), etc.:  40%|████      | 6/15 [00:00<00:00, 56.16it/s]
Animation 0: FadeIn(VGroup of 5 submobjects), etc.:  80%|████████  | 12/15 [00:00<00:00, 55.68it/s]
                                                                                                   
[10/10/26 20:35:54] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/3                         
                             429491395_2714580601_42663                         
                             90780.mp4'                                         
                    INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_3109915768_37797                         
                             71117.mp4'                                         

Animation 2: FadeIn(Rectangle):   0%|          | 0/5 [00:00<?, ?it/s]
                                                                     
                    INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_865986260_646678                         
                             108.mp4'                                           
[10/10/26 20:35:55] INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_177655839_163848                         
                             7423.mp4'                                          

Animation 4: Create(VGroup of 2 submobjects):   0%|          | 0/8 [00:00<?, ?it/s]
                                                                                   
                    INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_2535448466_40152                         
                             51824.mp4'                                         
                    INFO     Animation 5 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_3960336620_11242                         
                             15511.mp4'                                         

Animation 6: _MethodAnimation(Rectangle):   0%|          | 0/5 [00:00<?, ?it/s]
                                                                               
[10/10/26 20:35:56] INFO     Animation 6 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_2955544585_29688                         
                             22359.mp4'                                         
                    INFO     Animation 7 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_1892818439_23856                         
                             95228.mp4'                                         

Animation 8: Create(VGroup of 2 submobjects):   0%|          | 0/8 [00:00<?, ?it/s]
                                                                                   
                    INFO     Animation 8 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_2031239149_40509                         
                             46563.mp4'                                         
                    INFO     Animation 9 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_3919937666_54250                         
                             4041.mp4'                                          

Animation 10: _MethodAnimation(Rectangle):   0%|          | 0/5 [00:00<?, ?it/s]
                                                                                
[10/10/26 20:35:57] INFO     Animation 10 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_1412001765_38536                         
                             34062.mp4'                                         
                    INFO     Animation 11 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_273539326_814460                         
                             634.mp4'                                           

Animation 12: Create(VGroup of 2 submobjects), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
                                                                                           
                    INFO     Animation 12 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_3404217500_74014                         
                             4302.mp4'                                          
[10/10/26 20:35:58] INFO     Animation 13 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_1904135597_10936                         
                             25430.mp4'                                         

Animation 14: _MethodAnimation(Rectangle):   0%|          | 0/5 [00:00<?, ?it/s]
                                                                                
                    INFO     Animation 14 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_3818482780_10010                         
                             0726.mp4'                                          
[10/10/26 20:35:59] INFO     Animation 15 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_3564030450_22971                         
                             38237.mp4'                                         

Animation 16: Create(VGroup of 2 submobjects):   0%|          | 0/8 [00:00<?, ?it/s]
                                                                                    
                    INFO     Animation 16 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_739974172_270916                         
                             2625.mp4'                                          
                    INFO     Animation 17 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_3192426735_50256                         
                             186.mp4'                                           

Animation 18: _MethodAnimation(Rectangle):   0%|          | 0/5 [00:00<?, ?it/s]
                                                                                
[10/10/26 20:36:00] INFO     Animation 18 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_1670409320_16141                         
                             93374.mp4'                                         
                    INFO     Animation 19 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_1840955815_83122                         
                             7413.mp4'                                          

Animation 20: Create(VGroup of 2 submobjects):   0%|          | 0/8 [00:00<?, ?it/s]
                                                                                    
                    INFO     Animation 20 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_1519353049_32050                         
                             27448.mp4'                                         

Animation 21: _MethodAnimation(Rectangle):   0%|          | 0/5 [00:00<?, ?it/s]
                                                                                
                    INFO     Animation 21 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_4208325328_22030                         
                             89957.mp4'                                         
[10/10/26 20:36:01] INFO     Animation 22 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B04_Browser/1                         
                             606801221_459491290_156836                         
                             0693.mp4'                                          
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B04_Bro                         
                             wser.mp4'                                          
                                                                                
                    INFO     Rendered B04_Browser                   scene.py:247
                             Played 23 animations                               
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim

Animation 0: FadeIn(VGroup of 5 submobjects), etc.:   0%|          | 0/9 [00:00<?, ?it/s]
                                                                                         
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 2: FadeIn(Rectangle):   0%|          | 0/3 [00:00<?, ?it/s]
                                                                     

Animation 4: Create(VGroup of 2 submobjects):   0%|          | 0/5 [00:00<?, ?it/s]
                                                                                   

Animation 6: _MethodAnimation(Rectangle):   0%|          | 0/3 [00:00<?, ?it/s]
                                                                               

Animation 8: Create(VGroup of 2 submobjects):   0%|          | 0/5 [00:00<?, ?it/s]
                                                                                   

Animation 10: _MethodAnimation(Rectangle):   0%|          | 0/3 [00:00<?, ?it/s]
                                                                                

Animation 12: Create(VGroup of 2 submobjects), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                          

Animation 14: _MethodAnimation(Rectangle):   0%|          | 0/3 [00:00<?, ?it/s]
                                                                                

Animation 16: Create(VGroup of 2 submobjects):   0%|          | 0/5 [00:00<?, ?it/s]
                                                                                    

Animation 18: _MethodAnimation(Rectangle):   0%|          | 0/3 [00:00<?, ?it/s]
                                                                                

Animation 20: Create(VGroup of 2 submobjects):   0%|          | 0/5 [00:00<?, ?it/s]
                                                                                    

Animation 21: _MethodAnimation(Rectangle):   0%|          | 0/3 [00:00<?, ?it/s]
                                                                                
[audit] scenes: 34 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[run] rendering B05_Checklist
Manim Community v0.18.1


Animation 0: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/15 [00:00<?, ?it/s]
Animation 0: FadeIn(VGroup of 2 submobjects), etc.:  60%|██████    | 9/15 [00:00<00:00, 89.31it/s]
                                                                                                  
[10/10/26 20:36:03] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B05_Checklist                         
                             /3429491395_1110008006_420                         
                             2040526.mp4'                                       
[10/10/26 20:36:04] INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B05_Checklist                         
                             /1606801221_429412781_1313                         
                             452743.mp4'                                        

Animation 2: LaggedStart(Group):   0%|          | 0/20 [00:00<?, ?it/s]
Animation 2: LaggedStart(Group):  60%|██████    | 12/20 [00:00<00:00, 113.41it/s]
                                                                                 
[10/10/26 20:36:05] INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B05_Checklist                         
                             /1606801221_4212008478_370                         
                             2633326.mp4'                                       
[10/10/26 20:36:06] INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B05_Checklist                         
                             /1606801221_479000723_2330                         
                             895462.mp4'                                        

Animation 4: FadeIn(Dot):   0%|          | 0/10 [00:00<?, ?it/s]
                                                                
                    INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B05_Checklist                         
                             /1606801221_1644740214_309                         
                             6146724.mp4'                                       
[10/10/26 20:36:07] INFO     Animation 5 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B05_Checklist                         
                             /1606801221_3036404045_298                         
                             1069284.mp4'                                       
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B05_Che                         
                             cklist.mp4'                                        
                                                                                
                    INFO     Rendered B05_Checklist                 scene.py:247
                             Played 6 animations                                
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim

Animation 0: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/9 [00:00<?, ?it/s]
                                                                                         
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 2: LaggedStart(Group):   0%|          | 0/12 [00:00<?, ?it/s]
                                                                       

Animation 4: FadeIn(Dot):   0%|          | 0/6 [00:00<?, ?it/s]
                                                               
[audit] scenes: 9 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[run] rendering B06_Landscape
Manim Community v0.18.1

[10/10/26 20:36:09] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B06_Landscape                         
                             /3429491395_3834051993_296                         
                             2242425.mp4'                                       

Animation 1: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/15 [00:00<?, ?it/s]
Animation 1: FadeIn(VGroup of 2 submobjects), etc.:  53%|█████▎    | 8/15 [00:00<00:00, 72.21it/s]
                                                                                                  
                    INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B06_Landscape                         
                             /1606801221_1439090329_258                         
                             0291040.mp4'                                       
[10/10/26 20:36:10] INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B06_Landscape                         
                             /1606801221_3669496627_368                         
                             8695336.mp4'                                       

Animation 3: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/15 [00:00<?, ?it/s]
Animation 3: FadeIn(VGroup of 2 submobjects), etc.:  53%|█████▎    | 8/15 [00:00<00:00, 71.82it/s]
                                                                                                  
[10/10/26 20:36:11] INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B06_Landscape                         
                             /1606801221_55353407_47014                         
                             4147.mp4'                                          
[10/10/26 20:36:13] INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B06_Landscape                         
                             /1606801221_2553200637_188                         
                             7311662.mp4'                                       

Animation 5: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
Animation 5: FadeIn(VGroup of 3 submobjects), etc.:  90%|█████████ | 9/10 [00:00<00:00, 86.93it/s]
                                                                                                  
                    INFO     Animation 5 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B06_Landscape                         
                             /1606801221_2645881760_284                         
                             2205052.mp4'                                       
[10/10/26 20:36:14] INFO     Animation 6 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B06_Landscape                         
                             /1606801221_3735081639_314                         
                             3198010.mp4'                                       

Animation 7: GrowArrow(Arrow), etc.:   0%|          | 0/15 [00:00<?, ?it/s]
Animation 7: GrowArrow(Arrow), etc.:  80%|████████  | 12/15 [00:00<00:00, 111.04it/s]
                                                                                     
[10/10/26 20:36:15] INFO     Animation 7 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B06_Landscape                         
                             /1606801221_4229862530_191                         
                             1712640.mp4'                                       
                    INFO     Animation 8 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B06_Landscape                         
                             /1606801221_2521058971_218                         
                             9834235.mp4'                                       
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B06_Lan                         
                             dscape.mp4'                                        
                                                                                
                    INFO     Rendered B06_Landscape                 scene.py:247
                             Played 9 animations                                
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 1: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/9 [00:00<?, ?it/s]
                                                                                         

Animation 3: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/9 [00:00<?, ?it/s]
                                                                                         

Animation 5: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                         

Animation 7: GrowArrow(Arrow), etc.:   0%|          | 0/9 [00:00<?, ?it/s]
                                                                          
[audit] scenes: 14 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[run] rendering B07_Examples
Manim Community v0.18.1


Animation 0: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/15 [00:00<?, ?it/s]
Animation 0: FadeIn(VGroup of 2 submobjects), etc.:  47%|████▋     | 7/15 [00:00<00:00, 64.37it/s]
Animation 0: FadeIn(VGroup of 2 submobjects), etc.:  93%|█████████▎| 14/15 [00:00<00:00, 65.82it/s]
                                                                                                   
[10/10/26 20:36:17] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B07_Examples/                         
                             3429491395_3544060076_2441                         
                             170173.mp4'                                        
[10/10/26 20:36:19] INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B07_Examples/                         
                             1606801221_1998658364_3512                         
                             59819.mp4'                                         

Animation 2: FadeIn(Polygon):   0%|          | 0/10 [00:00<?, ?it/s]
                                                                    
                    INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B07_Examples/                         
                             1606801221_3636393217_1521                         
                             171352.mp4'                                        
[10/10/26 20:36:20] INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B07_Examples/                         
                             1606801221_643281955_28224                         
                             69997.mp4'                                         

Animation 4: LaggedStart(Group):   0%|          | 0/24 [00:00<?, ?it/s]
Animation 4: LaggedStart(Group):  50%|█████     | 12/24 [00:00<00:00, 113.92it/s]
Animation 4: LaggedStart(Group): 100%|██████████| 24/24 [00:00<00:00, 114.87it/s]
                                                                                 
                    INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B07_Examples/                         
                             1606801221_2858267685_4755                         
                             56093.mp4'                                         
[10/10/26 20:36:21] INFO     Animation 5 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B07_Examples/                         
                             1606801221_537206010_22480                         
                             89758.mp4'                                         
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B07_Exa                         
                             mples.mp4'                                         
                                                                                
                    INFO     Rendered B07_Examples                  scene.py:247
                             Played 6 animations                                
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim

Animation 0: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/9 [00:00<?, ?it/s]
                                                                                         
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 2: FadeIn(Polygon):   0%|          | 0/6 [00:00<?, ?it/s]
                                                                   

Animation 4: LaggedStart(Group):   0%|          | 0/15 [00:00<?, ?it/s]
                                                                       
[audit] scenes: 9 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[run] rendering B08_Skills
Manim Community v0.18.1

[10/10/26 20:36:23] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B08_Skills/34                         
                             29491395_2083261923_232311                         
                             0678.mp4'                                          

Animation 1: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
Animation 1: FadeIn(VGroup of 2 submobjects), etc.:  90%|█████████ | 9/10 [00:00<00:00, 84.73it/s]
                                                                                                  
                    INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B08_Skills/16                         
                             06801221_945210278_1296408                         
                             670.mp4'                                           
[10/10/26 20:36:24] INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B08_Skills/16                         
                             06801221_2997717298_320669                         
                             0764.mp4'                                          

Animation 3: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
                                                                                          
                    INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B08_Skills/16                         
                             06801221_3364606670_255789                         
                             2909.mp4'                                          
                    INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B08_Skills/16                         
                             06801221_4284081518_816832                         
                             359.mp4'                                           

Animation 5: LaggedStart(Group), etc.:   0%|          | 0/12 [00:00<?, ?it/s]
Animation 5: LaggedStart(Group), etc.:  92%|█████████▏| 11/12 [00:00<00:00, 101.91it/s]
                                                                                       
                    INFO     Animation 5 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B08_Skills/16                         
                             06801221_4280821732_168165                         
                             9906.mp4'                                          
[10/10/26 20:36:25] INFO     Animation 6 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B08_Skills/16                         
                             06801221_3636323336_119951                         
                             2694.mp4'                                          

Animation 7: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
Animation 7: FadeIn(VGroup of 3 submobjects), etc.: 100%|██████████| 10/10 [00:00<00:00, 92.73it/s]
                                                                                                   
                    INFO     Animation 7 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B08_Skills/16                         
                             06801221_45302235_17838154                         
                             02.mp4'                                            
[10/10/26 20:36:28] INFO     Animation 8 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B08_Skills/16                         
                             06801221_960209525_1547215                         
                             412.mp4'                                           
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B08_Ski                         
                             lls.mp4'                                           
                                                                                
                    INFO     Rendered B08_Skills                    scene.py:247
                             Played 9 animations                                
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 1: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                         

Animation 3: FadeIn(VGroup of 2 submobjects), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                         

Animation 5: LaggedStart(Group), etc.:   0%|          | 0/8 [00:00<?, ?it/s]
                                                                            

Animation 7: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                         
[audit] scenes: 14 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[run] rendering B09_Fields
Manim Community v0.18.1

[10/10/26 20:36:29] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/34                         
                             29491395_3333906860_294508                         
                             9165.mp4'                                          

Animation 1: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
Animation 1: FadeIn(VGroup of 3 submobjects), etc.: 100%|██████████| 10/10 [00:00<00:00, 95.78it/s]
                                                                                                   
                    INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/16                         
                             06801221_2129079469_269860                         
                             158.mp4'                                           
[10/10/26 20:36:30] INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/16                         
                             06801221_844001500_9858488                         
                             14.mp4'                                            

Animation 3: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
Animation 3: FadeIn(VGroup of 3 submobjects), etc.: 100%|██████████| 10/10 [00:00<00:00, 99.03it/s]
                                                                                                   
                    INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/16                         
                             06801221_779510472_1622236                         
                             811.mp4'                                           
                    INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/16                         
                             06801221_4084508497_262126                         
                             4867.mp4'                                          

Animation 5: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
                                                                                          
                    INFO     Animation 5 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/16                         
                             06801221_3861263893_150207                         
                             2846.mp4'                                          
[10/10/26 20:36:31] INFO     Animation 6 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/16                         
                             06801221_2451365586_232954                         
                             4591.mp4'                                          
                    INFO     Animation 7 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/16                         
                             06801221_2936675101_150676                         
                             8839.mp4'                                          

Animation 8: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
                                                                                          
                    INFO     Animation 8 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/16                         
                             06801221_1798545375_167861                         
                             5518.mp4'                                          
[10/10/26 20:36:32] INFO     Animation 9 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/16                         
                             06801221_3350860122_173345                         
                             597.mp4'                                           
                    INFO     Animation 10 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/16                         
                             06801221_3291324218_982684                         
                             183.mp4'                                           

Animation 11: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
                                                                                           
                    INFO     Animation 11 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/16                         
                             06801221_910590647_3950476                         
                             394.mp4'                                           
[10/10/26 20:36:33] INFO     Animation 12 : Partial     scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B09_Fields/16                         
                             06801221_3222987261_921871                         
                             060.mp4'                                           
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B09_Fie                         
                             lds.mp4'                                           
                                                                                
                    INFO     Rendered B09_Fields                    scene.py:247
                             Played 13 animations                               
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 1: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                         

Animation 3: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                         

Animation 5: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                         

Animation 8: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                         

Animation 11: FadeIn(VGroup of 3 submobjects), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                          
[audit] scenes: 21 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[run] rendering B10_ScopeTest
Manim Community v0.18.1


Animation 0: FadeIn(VGroup of 4 submobjects):   0%|          | 0/12 [00:00<?, ?it/s]
Animation 0: FadeIn(VGroup of 4 submobjects):  58%|█████▊    | 7/12 [00:00<00:00, 63.84it/s]
                                                                                            
[10/10/26 20:36:34] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B10_ScopeTest                         
                             /3429491395_2002912992_391                         
                             8378095.mp4'                                       

Animation 1: LaggedStart(Group):   0%|          | 0/20 [00:00<?, ?it/s]
Animation 1: LaggedStart(Group):  60%|██████    | 12/20 [00:00<00:00, 115.14it/s]
                                                                                 
[10/10/26 20:36:35] INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B10_ScopeTest                         
                             /1606801221_2790527229_380                         
                             9696053.mp4'                                       
[10/10/26 20:36:37] INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B10_ScopeTest                         
                             /1606801221_1508778931_342                         
                             5886790.mp4'                                       
                    INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B10_ScopeTest                         
                             /1606801221_3434561172_283                         
                             4762268.mp4'                                       

Animation 4: FadeIn(VGroup of 10 submobjects), etc.:   0%|          | 0/12 [00:00<?, ?it/s]
Animation 4: FadeIn(VGroup of 10 submobjects), etc.:  83%|████████▎ | 10/12 [00:00<00:00, 96.98it/s]
                                                                                                    
                    INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B10_ScopeTest                         
                             /1606801221_1714828833_294                         
                             8338381.mp4'                                       
[10/10/26 20:36:38] INFO     Animation 5 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B10_ScopeTest                         
                             /1606801221_1399164696_124                         
                             2021648.mp4'                                       

Animation 6: FadeIn(VGroup of 3 submobjects):   0%|          | 0/10 [00:00<?, ?it/s]
                                                                                    
                    INFO     Animation 6 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B10_ScopeTest                         
                             /1606801221_781638804_3125                         
                             081491.mp4'                                        
[10/10/26 20:36:39] INFO     Animation 7 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B10_ScopeTest                         
                             /1606801221_3063817253_582                         
                             518738.mp4'                                        

Animation 8: LaggedStart(Group):   0%|          | 0/20 [00:00<?, ?it/s]
Animation 8: LaggedStart(Group):  60%|██████    | 12/20 [00:00<00:00, 116.20it/s]
                                                                                 
[10/10/26 20:36:40] INFO     Animation 8 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B10_ScopeTest                         
                             /1606801221_3613798773_193                         
                             4059806.mp4'                                       
[10/10/26 20:36:41] INFO     Animation 9 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B10_ScopeTest                         
                             /1606801221_1168403021_184                         
                             3230044.mp4'                                       
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B10_Sco                         
                             peTest.mp4'                                        
                                                                                
                    INFO     Rendered B10_ScopeTest                 scene.py:247
                             Played 10 animations                               
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim

Animation 0: FadeIn(VGroup of 4 submobjects):   0%|          | 0/8 [00:00<?, ?it/s]
                                                                                   

Animation 1: LaggedStart(Group):   0%|          | 0/12 [00:00<?, ?it/s]
                                                                       
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 4: FadeIn(VGroup of 10 submobjects), etc.:   0%|          | 0/8 [00:00<?, ?it/s]
                                                                                          

Animation 6: FadeIn(VGroup of 3 submobjects):   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                   

Animation 8: LaggedStart(Group):   0%|          | 0/12 [00:00<?, ?it/s]
                                                                       
[audit] scenes: 15 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[run] rendering B11_Shrink
Manim Community v0.18.1


Animation 0: FadeIn(VGroup of 2 submobjects):   0%|          | 0/12 [00:00<?, ?it/s]
Animation 0: FadeIn(VGroup of 2 submobjects):  83%|████████▎ | 10/12 [00:00<00:00, 92.63it/s]
                                                                                             
[10/10/26 20:36:42] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B11_Shrink/34                         
                             29491395_616798995_4202040                         
                             526.mp4'                                           
[10/10/26 20:36:43] INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B11_Shrink/16                         
                             06801221_4205392534_187684                         
                             2060.mp4'                                          

Animation 2: FadeIn(Polygon), etc.:   0%|          | 0/24 [00:00<?, ?it/s]
Animation 2: FadeIn(Polygon), etc.:  42%|████▏     | 10/24 [00:00<00:00, 95.26it/s]
Animation 2: FadeIn(Polygon), etc.:  88%|████████▊ | 21/24 [00:00<00:00, 102.24it/s]
                                                                                    
[10/10/26 20:36:44] INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B11_Shrink/16                         
                             06801221_3891216539_414885                         
                             2451.mp4'                                          

Animation 3: FadeIn(Text('smaller problem?')):   0%|          | 0/10 [00:00<?, ?it/s]
Animation 3: FadeIn(Text('smaller problem?')): 100%|██████████| 10/10 [00:00<00:00, 97.84it/s]
                                                                                              
                    INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B11_Shrink/16                         
                             06801221_1579410793_702909                         
                             562.mp4'                                           
[10/10/26 20:36:47] INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B11_Shrink/16                         
                             06801221_2580693517_217996                         
                             1735.mp4'                                          
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B11_Shr                         
                             ink.mp4'                                           
                                                                                
                    INFO     Rendered B11_Shrink                    scene.py:247
                             Played 5 animations                                
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim

Animation 0: FadeIn(VGroup of 2 submobjects):   0%|          | 0/8 [00:00<?, ?it/s]
                                                                                   
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 2: FadeIn(Polygon), etc.:   0%|          | 0/15 [00:00<?, ?it/s]
                                                                          

Animation 3: FadeIn(Text('smaller problem?')):   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                    
[audit] scenes: 7 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[run] rendering B12_GitLog
Manim Community v0.18.1


Animation 0: Create(Line):   0%|          | 0/20 [00:00<?, ?it/s]
Animation 0: Create(Line):  60%|██████    | 12/20 [00:00<00:00, 112.74it/s]
                                                                           
[10/10/26 20:36:48] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B12_GitLog/34                         
                             29491395_3674035176_126944                         
                             5908.mp4'                                          
[10/10/26 20:36:50] INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B12_GitLog/16                         
                             06801221_4208682823_241175                         
                             2061.mp4'                                          

Animation 2: FadeIn(Dot), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
Animation 2: FadeIn(Dot), etc.: 100%|██████████| 10/10 [00:00<00:00, 94.95it/s]
                                                                               
                    INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B12_GitLog/16                         
                             06801221_3474196150_313104                         
                             3197.mp4'                                          
                    INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B12_GitLog/16                         
                             06801221_79640510_36900341                         
                             65.mp4'                                            

Animation 4: FadeIn(Dot), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
Animation 4: FadeIn(Dot), etc.: 100%|██████████| 10/10 [00:00<00:00, 98.61it/s]
                                                                               
[10/10/26 20:36:51] INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B12_GitLog/16                         
                             06801221_2479444758_243592                         
                             0114.mp4'                                          
                    INFO     Animation 5 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B12_GitLog/16                         
                             06801221_79640510_14640472                         
                             66.mp4'                                            

Animation 6: FadeIn(Dot), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
Animation 6: FadeIn(Dot), etc.: 100%|██████████| 10/10 [00:00<00:00, 95.47it/s]
                                                                               
                    INFO     Animation 6 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B12_GitLog/16                         
                             06801221_3853582100_247405                         
                             9121.mp4'                                          
                    INFO     Animation 7 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B12_GitLog/16                         
                             06801221_79640510_35780232                         
                             36.mp4'                                            

Animation 8: FadeIn(Dot), etc.:   0%|          | 0/10 [00:00<?, ?it/s]
                                                                      
[10/10/26 20:36:52] INFO     Animation 8 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B12_GitLog/16                         
                             06801221_878514345_3564783                         
                             135.mp4'                                           
[10/10/26 20:36:53] INFO     Animation 9 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B12_GitLog/16                         
                             06801221_1703374595_361172                         
                             9827.mp4'                                          
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B12_Git                         
                             Log.mp4'                                           
                                                                                
                    INFO     Rendered B12_GitLog                    scene.py:247
                             Played 10 animations                               
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim

Animation 0: Create(Line):   0%|          | 0/12 [00:00<?, ?it/s]
                                                                 
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 2: FadeIn(Dot), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                     

Animation 4: FadeIn(Dot), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                     

Animation 6: FadeIn(Dot), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                     

Animation 8: FadeIn(Dot), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                     
[audit] scenes: 15 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[remotion] B14: filled already (skip)
[remotion] done — run `bash scripts/run.sh <REEL>` to compile the cut
[art] compiled B01  MANIM     6.5s  ← B01.mp4
[art] compiled B02  MANIM     8.9s  ← B02.mp4
[art] compiled B03  MANIM    10.0s  ← B03.mp4
[art] compiled B04  MANIM    13.8s  ← B04.mp4
[art] compiled B05  MANIM    12.7s  ← B05.mp4
[art] compiled B06  MANIM    21.0s  ← B06.mp4
[art] compiled B07  MANIM    13.5s  ← B07.mp4
[art] compiled B08  MANIM    17.5s  ← B08.mp4
[art] compiled B09  MANIM     7.0s  ← B09.mp4
[art] compiled B10  MANIM    17.6s  ← B10.mp4
[art] compiled B11  MANIM    18.0s  ← B11.mp4
[art] compiled B12  MANIM    14.4s  ← B12.mp4
[art] motion histogram: graphic:13  remotion:1
[art] build stamp → beat_sheet.json (14/14 filled)
[art] QC contact sheet → <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/qc-sheet.png
[art] wrote <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/gistgap-pitch-slate.mp4  (175.5s, audio: per-beat timeline (source audio preserved), drawtext: no — PIL overlays)
[art] slots: 14/14 filled — B01:MANIM B02:MANIM B03:MANIM B04:MANIM B05:MANIM B06:MANIM B07:MANIM B08:MANIM B09:MANIM B10:MANIM B11:MANIM B12:MANIM B13:MANIM B14:VIDEO
[run] GATE V — frame-level visual QC on the compiled reel
[gate-v] frames=28 BLOCKER=0 MAJOR=0 → <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/_qc/REPORT.md
[run] done → <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film  (QC gates: on)
[run] REVIEW built; no final exported. Use ./art final <reel> for a verified master.
[run] any remaining slates are YOUR slots — see <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/SHOTLIST.md
### RUN EXIT=0 ELAPSED=161s
### ./art todo <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film
[todo] final-project-film: 14/14 filled → todo.json + STATUS.md + ToDo.md
    B01  filled     manim             pipeline manim/B01.mp4
    B02  filled     manim             pipeline manim/B02.mp4
    B03  filled     manim             pipeline manim/B03.mp4
    B04  filled     manim             pipeline manim/B04.mp4
    B05  filled     manim             pipeline manim/B05.mp4
    B06  filled     manim             pipeline manim/B06.mp4
    B07  filled     manim             pipeline manim/B07.mp4
    B08  filled     manim             pipeline manim/B08.mp4
    B09  filled     manim             pipeline manim/B09.mp4
    B10  filled     manim             pipeline manim/B10.mp4
    B11  filled     manim             pipeline manim/B11.mp4
    B12  filled     manim             pipeline manim/B12.mp4
    B13  filled     manim             pipeline manim/B13.mp4
    B14  filled     remotion          pipeline media/B14.mp4
### TODO EXIT=0 ELAPSED=0s
```

## gistgap-run5.log

Run 5 — B14 rebuild (2026-10-10): B14 re-rendered as a drawn title scene (B14_Title); B01–B13 reused unchanged.

```text
### ./art run <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film --height 2160
[run] skip B01_Agent — B01 already filled
[run] skip B02_ShownSigned — B02 already filled
[run] skip B03_Contract — B03 already filled
[run] skip B04_Browser — B04 already filled
[run] skip B05_Checklist — B05 already filled
[run] skip B06_Landscape — B06 already filled
[run] skip B07_Examples — B07 already filled
[run] skip B08_Skills — B08 already filled
[run] skip B09_Fields — B09 already filled
[run] skip B10_ScopeTest — B10 already filled
[run] skip B11_Shrink — B11 already filled
[run] skip B12_GitLog — B12 already filled
[run] skip B13_Columns — B13 already filled
[run] GATE L — beat-mix lint
[beat-lint] clean — beat mix OK (beat_sheet.json)
[run] GATE SHAPE — finance chart-shape enforcement
[gate-shape] skip — not a finance reel (beat_sheet.json)
[run] GATE A — static pre-flight

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[run] GATE W — WCAG contrast + margins + text-overlap (independent second check)
[gateW] B14_Title clean
[run] rendering B14_Title
Manim Community v0.18.1


Animation 0: FadeIn(Text('GistGap')):   0%|          | 0/9 [00:00<?, ?it/s]
                                                                           
[10/10/26 21:18:16] INFO     Animation 0 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B14_Title/342                         
                             9491395_1192041580_2231324                         
                             57.mp4'                                            

Animation 1: Create(Line), etc.:   0%|          | 0/9 [00:00<?, ?it/s]
Animation 1: Create(Line), etc.: 100%|██████████| 9/9 [00:00<00:00, 85.18it/s]
                                                                              
[10/10/26 21:18:17] INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B14_Title/160                         
                             6801221_3391914064_4217063                         
                             669.mp4'                                           
                    INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B14_Title/160                         
                             6801221_3175144691_3490589                         
                             903.mp4'                                           
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B14_Tit                         
                             le.mp4'                                            
                                                                                
                    INFO     Rendered B14_Title                     scene.py:247
                             Played 3 animations                                
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim

Animation 0: FadeIn(Text('GistGap')):   0%|          | 0/6 [00:00<?, ?it/s]
                                                                           

Animation 1: Create(Line), etc.:   0%|          | 0/6 [00:00<?, ?it/s]
                                                                      
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:
[audit] scenes: 4 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[remotion] nothing to do — no shot.remotion.pattern beats
[art] compiled B14  MANIM     2.3s  ← B14.mp4
[art] motion histogram: graphic:14
[art] build stamp → beat_sheet.json (14/14 filled)
[art] QC contact sheet → <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/qc-sheet.png
[art] wrote <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/gistgap-pitch-slate.mp4  (175.5s, audio: per-beat timeline (source audio preserved), drawtext: no — PIL overlays)
[art] slots: 14/14 filled — B01:MANIM B02:MANIM B03:MANIM B04:MANIM B05:MANIM B06:MANIM B07:MANIM B08:MANIM B09:MANIM B10:MANIM B11:MANIM B12:MANIM B13:MANIM B14:MANIM
[run] GATE V — frame-level visual QC on the compiled reel
[gate-v] frames=28 BLOCKER=0 MAJOR=0 → <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/_qc/REPORT.md
[run] done → <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film  (QC gates: on)
[run] REVIEW built; no final exported. Use ./art final <reel> for a verified master.
[run] any remaining slates are YOUR slots — see <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/SHOTLIST.md
### RUN EXIT=0 ELAPSED=56s
### ./art todo <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film
[todo] final-project-film: 14/14 filled → todo.json + STATUS.md + ToDo.md
    B01  filled     manim             pipeline manim/B01.mp4
    B02  filled     manim             pipeline manim/B02.mp4
    B03  filled     manim             pipeline manim/B03.mp4
    B04  filled     manim             pipeline manim/B04.mp4
    B05  filled     manim             pipeline manim/B05.mp4
    B06  filled     manim             pipeline manim/B06.mp4
    B07  filled     manim             pipeline manim/B07.mp4
    B08  filled     manim             pipeline manim/B08.mp4
    B09  filled     manim             pipeline manim/B09.mp4
    B10  filled     manim             pipeline manim/B10.mp4
    B11  filled     manim             pipeline manim/B11.mp4
    B12  filled     manim             pipeline manim/B12.mp4
    B13  filled     manim             pipeline manim/B13.mp4
    B14  filled     manim             pipeline manim/B14.mp4
### TODO EXIT=0 ELAPSED=0s
```

## gistgap-final-fail1.log

Final export attempt 1 (2026-10-10): `./art final <reel> --height 2160 --out <reel>/exports/landscape` stopped at GATE T on B11 (bbox-overlap §8.6b); no master was written.

```text
### ./art final <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film --height 2160 --out <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/exports/landscape
[typecheck] wrote <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/TYPECHECK.md
[typecheck] §8.10 B01: SKIP
[typecheck] §8.10 B02: SKIP
[typecheck] §8.10 B03: SKIP
[typecheck] §8.10 B04: SKIP
[typecheck] §8.10 B05: SKIP
[typecheck] §8.10 B06: SKIP
[typecheck] §8.10 B07: SKIP
[typecheck] §8.10 B08: SKIP
[typecheck] §8.10 B09: SKIP
[typecheck] §8.10 B10: SKIP
[typecheck] §8.10 B11: SKIP
[typecheck] §8.10 B12: SKIP
[typecheck] §8.10 B13: SKIP
[typecheck] §8.10 B14: SKIP
[typecheck] GATE T: FAIL (1 pixel beats, 0 sweep, 0 shape)
[art final] GATE T BLOCKED: TYPECHECK.md has FAILs — fix before final cut.
[art final] See: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/TYPECHECK.md
### FINAL EXIT=2 ELAPSED=34s
```

## gistgap-run6.log

B11 rebuild, review build (2026-10-10): B11 re-rendered after its base was scaled with the box; the other 13 beats reused.

```text
### ./art run <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film --height 2160
[run] skip B01_Agent — B01 already filled
[run] skip B02_ShownSigned — B02 already filled
[run] skip B03_Contract — B03 already filled
[run] skip B04_Browser — B04 already filled
[run] skip B05_Checklist — B05 already filled
[run] skip B06_Landscape — B06 already filled
[run] skip B07_Examples — B07 already filled
[run] skip B08_Skills — B08 already filled
[run] skip B09_Fields — B09 already filled
[run] skip B10_ScopeTest — B10 already filled
[run] skip B12_GitLog — B12 already filled
[run] skip B13_Columns — B13 already filled
[run] skip B14_Title — B14 already filled
[run] GATE L — beat-mix lint
[beat-lint] clean — beat mix OK (beat_sheet.json)
[run] GATE SHAPE — finance chart-shape enforcement
[gate-shape] skip — not a finance reel (beat_sheet.json)
[run] GATE A — static pre-flight

[static-check] 1 scene(s): 1 clean · 0 warn · 0 error
[run] GATE W — WCAG contrast + margins + text-overlap (independent second check)
[gateW] B11_Shrink clean
[run] rendering B11_Shrink
Manim Community v0.18.1

[10/10/26 22:05:21] INFO     Animation 0 : Using cached     cairo_renderer.py:88
                             data (hash :                                       
                             3429491395_616798995_420204052                     
                             6)                                                 

Animation 0: FadeIn(VGroup of 2 submobjects):   0%|          | 0/1 [00:00<?, ?it/s]
                                                                                   
[10/10/26 22:05:22] INFO     Animation 1 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B11_Shrink/16                         
                             06801221_4205392534_149277                         
                             0448.mp4'                                          

Animation 2: FadeIn(Polygon), etc.:   0%|          | 0/24 [00:00<?, ?it/s]
Animation 2: FadeIn(Polygon), etc.:  42%|████▏     | 10/24 [00:00<00:00, 94.88it/s]
Animation 2: FadeIn(Polygon), etc.:  88%|████████▊ | 21/24 [00:00<00:00, 101.39it/s]
                                                                                    
[10/10/26 22:05:23] INFO     Animation 2 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B11_Shrink/16                         
                             06801221_624033982_3280899                         
                             567.mp4'                                           

Animation 3: FadeIn(Text('smaller problem?')):   0%|          | 0/10 [00:00<?, ?it/s]
Animation 3: FadeIn(Text('smaller problem?')): 100%|██████████| 10/10 [00:00<00:00, 98.10it/s]
                                                                                              
                    INFO     Animation 3 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B11_Shrink/16                         
                             06801221_1579410793_393440                         
                             785.mp4'                                           
[10/10/26 22:05:25] INFO     Animation 4 : Partial      scene_file_writer.py:527
                             movie file written in                              
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/partial                         
                             _movie_files/B11_Shrink/16                         
                             06801221_2580693517_251366                         
                             8269.mp4'                                          
                    INFO     Combining to Movie file.   scene_file_writer.py:617
                    INFO                                scene_file_writer.py:737
                             File ready at                                      
                             '<home>/Docum                         
                             ents/Code/info-7375-prompt                         
                             -engineering-for-generativ                         
                             e-ai/fall-2026/prasad-s/fi                         
                             nal-project-film/media/vid                         
                             eos/scenes/2160p24/B11_Shr                         
                             ink.mp4'                                           
                                                                                
                    INFO     Rendered B11_Shrink                    scene.py:247
                             Played 5 animations                                
You are using manim version v0.18.1, but version v0.22.0 is available.
You should consider upgrading via pip install -U manim

Animation 0: FadeIn(VGroup of 2 submobjects):   0%|          | 0/8 [00:00<?, ?it/s]
                                                                                   
<home>/Documents/Code/brutalist.art/runtime/qc/manim_layout_audit.py:149: DeprecationWarning: This method is not guaranteed to stay around. Please prefer getting the attribute normally.
  if float(mob.get_stroke_opacity()) <= 0.02:

Animation 2: FadeIn(Polygon), etc.:   0%|          | 0/15 [00:00<?, ?it/s]
                                                                          

Animation 3: FadeIn(Text('smaller problem?')):   0%|          | 0/6 [00:00<?, ?it/s]
                                                                                    
[audit] scenes: 7 snapshots → CLEAN
[audit] report: <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/layout_audit.md
[remotion] nothing to do — no shot.remotion.pattern beats
[art] compiled B11  MANIM    18.0s  ← B11.mp4
[art] motion histogram: graphic:14
[art] build stamp → beat_sheet.json (14/14 filled)
[art] QC contact sheet → <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/qc-sheet.png
[art] wrote <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/gistgap-pitch-slate.mp4  (175.5s, audio: per-beat timeline (source audio preserved), drawtext: no — PIL overlays)
[art] slots: 14/14 filled — B01:MANIM B02:MANIM B03:MANIM B04:MANIM B05:MANIM B06:MANIM B07:MANIM B08:MANIM B09:MANIM B10:MANIM B11:MANIM B12:MANIM B13:MANIM B14:MANIM
[run] GATE V — frame-level visual QC on the compiled reel
[gate-v] frames=28 BLOCKER=0 MAJOR=0 → <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/_qc/REPORT.md
[run] done → <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film  (QC gates: on)
[run] REVIEW built; no final exported. Use ./art final <reel> for a verified master.
[run] any remaining slates are YOUR slots — see <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/SHOTLIST.md
### RUN EXIT=0 ELAPSED=63s
### ./art todo <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film
[todo] final-project-film: 14/14 filled → todo.json + STATUS.md + ToDo.md
    B01  filled     manim             pipeline manim/B01.mp4
    B02  filled     manim             pipeline manim/B02.mp4
    B03  filled     manim             pipeline manim/B03.mp4
    B04  filled     manim             pipeline manim/B04.mp4
    B05  filled     manim             pipeline manim/B05.mp4
    B06  filled     manim             pipeline manim/B06.mp4
    B07  filled     manim             pipeline manim/B07.mp4
    B08  filled     manim             pipeline manim/B08.mp4
    B09  filled     manim             pipeline manim/B09.mp4
    B10  filled     manim             pipeline manim/B10.mp4
    B11  filled     manim             pipeline manim/B11.mp4
    B12  filled     manim             pipeline manim/B12.mp4
    B13  filled     manim             pipeline manim/B13.mp4
    B14  filled     manim             pipeline manim/B14.mp4
### TODO EXIT=0 ELAPSED=0s
```

## gistgap-final2.log

Final export attempt 2 (2026-10-10): GATE T passed on all 14 beats and the master was written.

```text
### ./art final <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film --height 2160 --out <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/exports/landscape
[typecheck] wrote <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/TYPECHECK.md
[typecheck] §8.10 B01: SKIP
[typecheck] §8.10 B02: SKIP
[typecheck] §8.10 B03: SKIP
[typecheck] §8.10 B04: SKIP
[typecheck] §8.10 B05: SKIP
[typecheck] §8.10 B06: SKIP
[typecheck] §8.10 B07: SKIP
[typecheck] §8.10 B08: SKIP
[typecheck] §8.10 B09: SKIP
[typecheck] §8.10 B10: SKIP
[typecheck] §8.10 B11: SKIP
[typecheck] §8.10 B12: SKIP
[typecheck] §8.10 B13: SKIP
[typecheck] §8.10 B14: SKIP
[typecheck] GATE T: PASS
[art] motion histogram: graphic:14
[art] build stamp → beat_sheet.json (14/14 filled)
[art] wrote <home>/Documents/Code/info-7375-prompt-engineering-for-generative-ai/fall-2026/prasad-s/final-project-film/exports/landscape/gistgap-pitch.mp4  (175.5s, audio: per-beat timeline (source audio preserved), drawtext: no — PIL overlays)
[art] slots: 14/14 filled — B01:MANIM B02:MANIM B03:MANIM B04:MANIM B05:MANIM B06:MANIM B07:MANIM B08:MANIM B09:MANIM B10:MANIM B11:MANIM B12:MANIM B13:MANIM B14:MANIM
### FINAL EXIT=0 ELAPSED=87s
```

## Summary of the final master

- Master: `exports/landscape/gistgap-pitch.mp4`, 13,515,055 bytes, 175.458 s, 3840×2160, 24 fps; video h264 (High, yuv420p), audio AAC (LC, 48 kHz, stereo).
- SHA-256: `6a0329a02a36558ce1fbddda32adbafac63ceb398a3f3ee475fa320cd804ed04` (matches the `sha256` field of the export receipt).
- `master_check.py` passed (`[master] PASS  3840×2160  24fps  yuv420p  h264  175.5s`), but its duration assertion was skipped: `clock_check.py` is missing from the toolkit. Duration was instead checked with ffprobe against the 175.23 s beat total: 175.458 s, 0.228 s over, within 1 s.
- `receipts/gistgap-pitch.verified.redacted.json` and `receipts/MASTERCHECK.redacted.md` are copies of the export receipt and `MASTERCHECK.md` with the home-folder path replaced by `<home>`; nothing else was changed. The originals stay local and are ignored.
- `final-frames-contact.png` is an ffmpeg extract of one frame at 50% of each beat (B01–B14) from the master. It is not a gate report.
- The film itself is not in git; it is submitted in the Canvas zip.
- FACTCHECK.md verdicts are still PENDING.
