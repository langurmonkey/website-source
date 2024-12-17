#version 330 core

// Color buffer.
uniform sampler2D u_texture0;
// Depth buffer (log).
uniform sampler2D u_texture1;
// Position of our camera with respect to the object to render.
uniform vec3 u_pos;

// Texture coordinates.
in vec2 v_texCoords;
// Ray from camera to fragment.
in vec3 v_ray;

// Output color.
layout(location = 0) out vec4 fragColor;

void main() {
    // Ray direction.
    vec3 rayDir = normalize(v_ray);
    // Camera position.
    vec3 camPos = u_pos;
    // Position of object. We always put the position of the object at the origin.
    vec3 objPos = vec3(0.0, 0.0, 0.0);
    // Sample depth buffer.
    float depth = texture(u_texture1, v_texCoords).r;
    depth *= length(rayDir);
    // Color of pre-existing scene.
    vec3 col = texture(u_texture0, v_texCoords).rgb;

    // Here would go the call to ray-marching.

    // Finally, the blending would go here.
}
