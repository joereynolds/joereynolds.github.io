---
layout: default
tags: [programming]
---

# Burn
<div class="box blend-burn"></div>
<div class="box other-box"></div>

# Color
<div class="box blend-color"></div>
<div class="box other-box"></div>

# Darken
<div class="box blend-darken"></div>
<div class="box other-box"></div>

# Difference
<div class="box blend-difference"></div>
<div class="box other-box"></div>

# Dodge
<div class="box blend-dodge"></div>
<div class="box other-box"></div>

# Exclusion
<div class="box blend-exclusion"></div>
<div class="box other-box"></div>

# Hard Light
<div class="box blend-hard-light"></div>
<div class="box other-box"></div>

# Hue
<div class="box blend-hue"></div>
<div class="box other-box"></div>

# Lighten
<div class="box blend-lighten"></div>
<div class="box other-box"></div>

# Luminosity
<div class="box blend-luminosity"></div>
<div class="box other-box"></div>

# Multiply
<div class="box blend-multiply"></div>
<div class="box other-box"></div>

# Screen
<div class="box blend-screen"></div>
<div class="box other-box"></div>

# Soft Light
<div class="box blend-soft-light"></div>
<div class="box other-box"></div>

<style>
.box {
  display: inline-block;
  width: 150px;
  height: 150px;
  background: yellow;
  border-radius: 100%;
}

.other-box {
    margin-left: -50px;
    background: #ff9898;
}

.blend-burn {
    mix-blend-mode: color-burn;
}

.blend-color {
    mix-blend-mode: color;
}

.blend-darken {
    mix-blend-mode: darken;
}

.blend-difference {
    mix-blend-mode: difference;
}

.blend-dodge {
    mix-blend-mode: color-dodge;
}

.blend-exclusion {
    mix-blend-mode: exclusion;
}

.blend-hard-light {
    mix-blend-mode: hard-light;
}

.blend-hue {
    mix-blend-mode: hue;
}

.blend-lighten {
    mix-blend-mode: lighten;
}

.blend-luminosity {
    mix-blend-mode: luminosity;
}

.blend-multiply {
    mix-blend-mode: multiply;
}

.blend-screen {
    mix-blend-mode: screen;
}

.blend-soft-light {
    mix-blend-mode: soft-light;
}

</style>
