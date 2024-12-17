bool RaySphereIntersect(vec3 org, vec3 dir, out float near, out float far) {
    float b = dot(dir, org);
    float c = dot(org, org) - 8.0;
    float delta = b * b - c;
    if (delta < 0.0)
        return false;
    float deltasqrt = sqrt(delta);
    near = -b - deltasqrt;
    far = -b + deltasqrt;
    return far > 0.0;
}
