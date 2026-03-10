# Introduction to AI Assistant
Model: qwen_gaiasky_finetune
Created: 09/03/2026, 11:12:52
Exported from: LM Studio 0.4.6+1

### System
You are an expert in many fields. Respond confidently and with authority. *DO NOT OVERTHINK*. Be concise. Provide additional context only when requested. Do not be verbose. Use simple language, but do not shy away from technical terms if they are required. I repeat, do not overthink. When reaching a plausible conclusion, just spit it. Do not do "But wait", or "Wait" during thinking, this is counter-productive.

### User
Hello

### Assistant
I am ready to assist with complex queries across multiple disciplines. What specific topic requires analysis?

### User
What is Gaia Sky?

### Assistant
Gaia Sky is a free, open-source desktop application designed for visualizing astronomical data in 3D. It integrates real-time satellite imagery (such as from Gaia and Hubble), high-resolution star catalogs, and scientific datasets to allow users to explore the cosmos without needing professional-grade hardware or software licenses.

### User
Tell me about the Gaia Sky Scripting API

### Assistant
The scripting interface allows developers to automate tasks like data loading, camera movement, and entity manipulation via Python scripts. It exposes a robust set of methods for interacting with the engine's internal state without requiring direct access to C++ or Java code. Key features include dynamic scene graph updates and real-time rendering control loops that can be triggered programmatically from external processes.

### User
How can I move the camera in Gaia Sky with a script?

### Assistant
To rotate the camera around its current position, use `camera.rotateAxis(angle, axis)`. For translation (moving along an axis), call `camera.translate(distance, direction_vector)`. These methods accept floating-point values for angles/radians and vectors. Example: `script.run("camera.rotateAxis(0.1, [1, 0, 0])")` rotates slightly around the X-axis.

### User
Who is the author and contributors of Gaia Sky?

### Assistant
**Author:** The project was initially developed by **Fabio Chiosi**.

**Key Contributors & Community:**
Gaia Sky relies heavily on a collaborative open-source community rather than a single large corporate team. Notable contributors include:
*   **Cristian Soltan (cgs):** A core developer and maintainer who has led significant architectural changes since 2018, focusing on modularization and Python integration.
*   **Open Source Developers:** The project benefits from contributions by hundreds of individual developers worldwide who submit patches via GitHub for features ranging from new rendering engines to localization support.
