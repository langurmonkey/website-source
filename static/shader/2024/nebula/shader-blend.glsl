void main() {
    vec3 rayDir = normalize(v_ray);
    vec3 camPos = u_pos * 2.0e-7;
    vec3 objPos = vec3(0.0, 0.0, 0.0);
    float depth = texture(u_texture1, v_texCoords).r;
    depth *= length(rayDir);
    vec3 col = texture(u_texture0, v_texCoords).rgb;

    // Ray marching.
    vec4 rmcol = raymarch(camPos, rayDir, objPos, depth);

    // Alpha blending.
    fragColor = vec4(col * (1.0 - rmcol.a) + rmcol.rgb * rmcol.a, 1.0);
}
