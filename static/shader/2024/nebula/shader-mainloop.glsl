#define ITERATIONS 50

vec4 raymarch(vec3 camPos, vec3 rayDir, vec3 objPos, float depth) {
    // Ray direction.
    vec3 rd = rayDir;
    // Ray origin.
    vec3 ro = camPos;

    // ld, td: local, total density
    // w: weighting factor
    float ld = 0.0, td = 0.0, w = 0.0;

    // t: length of the ray
    // d: distance function
    float d = 1.0, t = 0.0;

    const float h = 0.1;

    vec4 sum = vec4(0.0);

    float min_dist = 0.0, max_dist = 0.0;

    // If our ray intersects the sphere...
    if (RaySphereIntersect(ro, rd, min_dist, max_dist)) {
        t = min_dist * step(t, min_dist);

        // Raymarch loop
        for (int i = 0; i < ITERATIONS; i++) {
            vec3 pos = ro + t * rd;

            // Loop break conditions.
            // Here we check the current distance agains the depth and the
            // maximum distance.
            if (t > depth || t > max_dist) break;

            // Evaluate distance function.
            // The map function returns the density at a given position.
            float d = map(pos);

            // Point light calculations.
            vec3 ldst = vec3(0.0) - pos;

            // Here, the color of light depends on the distance from the center
            // of the object. Typically, this is more complicated than what's here.
            vec3 lightColor = mix(colorA, colorB, ldst);

            if (d < h) {
                // Compute local density.
                ld = h - d;

                // Compute weighting factor.
                w = (1.0 - td) * ld;

                // Accumulate density.
                td += w + 1.0 / 200.0;

                vec4 col = vec4(0.3, 0.3, 0.3, td);

                // Emission.
                sum += sum.a * vec4(sum.rgb, 0.0) * 0.2;

                // Uniform scale density.
                col.a *= 0.2;
                // Colour by alpha.
                col.rgb *= col.a;
                // Alpha blend in contribution.
                sum = sum + col * (1.0 - sum.a);
            }
            td += 1.0 / 90.0;

            // Optimize step size near the camera.
            t += max(d * 0.1 * max(min(length(ldst), length(ro)), 1.0), 0.01);
        }

        // Simple scattering.
        sum *= 1. / exp(ld * 0.2) * 0.4;
        sum = clamp(sum, 0.0, 1.0);
        sum.xyz = sum.xyz * sum.xyz * (3.0 - 2.0 * sum.xyz);
    }
    return vec4(sum.xyz, td);
}
