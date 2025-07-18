
K���en_US����  ( 2opengl:OpenGLBOpenGL PluginJGeneralZ	composite�
[
texture_filter"Texture Filter*Texture filteringZ` hr FastrGoodrBest
F
lighting "Lighting*,Use diffuse light when screen is transformedZ 
c
sync_to_vblank "Sync To VBlank*;Only perform screen updates during vertical blanking periodZ
o
texture_compression "Texture Compression*?If available use compression for textures converted from imagesZ 
�
framebuffer_object "Framebuffer object*�Render all frames indirectly using framebuffer objects (GL_EXT_framebuffer_object), if supported by the driver. Pros: Might be faster than the default buffer swapping method in some cases. Cons: This will come at the cost of (1) usually reduced graphics benchmark performance; (2) increased GPU resource consumption; and (3) possibly higher visible lag. Note: This feature is always on in OpenGL|ES builds such as ARM platforms.Z
�
vertex_buffer_object "Vertex buffer object*�Render all graphics primitives using vertex buffer objects (GL_ARB_vertex_buffer_object), if supported by the driver. Pros: This provides higher graphics performance for some drivers. Cons: This is a new feature and may cause graphical problems. Note: This feature is always on in OpenGL|ES builds such as ARM platforms.Z
�
always_swap_buffers "Always use buffer swapping*�Use glXSwapBuffers to display every frame. This eliminates visible tearing with most drivers and dramatically improves visual smoothness. Automatically enabled when framebuffer_object is on.Z
�
unredirect_driver_blacklist"Unredirect Driver Blacklist*�If non-empty, specifies a POSIX (extended) regular expression to match against the OpenGL driver strings (newline separated): "GL_VENDOR\nGL_RENDERER\nGL_VERSION". If the regular expression matches a substring of that concatenation then no windows will ever be unredirected while using that particular graphics driver.Z2(nouveau|Intel).*Mesa 8.0
�
enable_x11_sync "Enabled*�Use X11 Sync fences to synchronize rendering between X11 and OpenGL (GL_EXT_x11_sync_object). Without this, the contents of windows may not be completely redrawn.0 Z
w
x11_sync_blacklist_vendor"Vendor*6The card vendor for which X11 sync should be disabled.0 8 Z2NVIDIAZ2NVIDIA
�
x11_sync_blacklist_model"Model*6The card vendor for which X11 sync should be disabled.0 8 Z2GeForce 6150(LE|SE)Z2GeForce (7025|7050 PV)X11 Sync ObjectsCards Blacklist