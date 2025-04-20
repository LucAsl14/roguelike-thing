#version 300 es
precision highp float;

vec2 vertices[4] = vec2[](
    vec2(-1.0, -1.0),
    vec2(-1.0, 1.0),
    vec2(1.0, -1.0),
    vec2(1.0, 1.0)
);

out vec2 pos;

void main() {
    gl_Position = vec4(vertices[gl_VertexID], 0.0, 1.0);
    pos = vertices[gl_VertexID] * 0.5 + 0.5;
}
