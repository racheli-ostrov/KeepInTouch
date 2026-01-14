# 🖐️ KeepInTouch - Hands-Free Email Controller

**KeepInTouch** is an innovative accessibility tool that allows users to manage their emails using hand gestures and voice commands. By leveraging Computer Vision and Speech-to-Text technology, it enables a completely touchless experience—perfect for users in the kitchen, students during remote learning, or anyone who needs to stay connected while their hands are busy.

---

## 🌟 Why KeepInTouch?

* **Touchless Interaction:** Control your workspace without touching the screen or keyboard.
* **Gesture Recognition:** Use intuitive hand signs to trigger actions (e.g., Like to compose, Dislike to send).
* **Voice-Powered Writing:** Dictate your messages naturally with integrated microphone support.
* **Audio Guidance:** The system reads out prompts and labels to guide you through the process.

---

## 🛠 Real-World Use Cases

* **🍳 In the Kitchen:** Reply to messages while cooking without worrying about flour or oil on your screen.
* **📚 Remote Learning:** Stay focused on your notes while managing notifications hands-free.
* **♿ Accessibility:** A powerful tool for individuals with limited mobility or motor impairments.

---

## ✨ Key Features

* **🖐️ Gesture Shortcuts:** * **👍 Thumbs Up:** Open a "New Mail" window.
    * **👎 Thumbs Down:** Send the current draft.
    * **...and more custom gestures.**
* **🎙️ Smart Dictation:** High-accuracy Speech-to-Text for composing email bodies and subject lines.
* **🔊 Text-to-Speech (TTS):** Audio feedback that reads out instructions and helps navigate the interface.
* **🤖 Computer Vision Engine:** Real-time hand tracking and gesture classification.

---

## 🏗 Technology Stack

* **AI & Logic:** Python / JavaScript (בחר את הרלוונטי)
* **Vision:** MediaPipe / OpenCV (לזיהוי תנועות ידיים)
* **Speech:** Web Speech API / Google Speech-to-Text
* **Communication:** SMTP / Gmail API / Outlook API
* **Frontend:** React (for the dashboard)

---

## 📁 System Architecture

The project follows a **Multimodal Interaction** workflow:
1.  **Video Stream:** Captures frames from the webcam.
2.  **Gesture Processing:** AI identifies landmarks on the hand and classifies the gesture.
3.  **Command Execution:** Triggers specific email API functions based on the gesture.
4.  **Voice Feedback:** TTS engine confirms the action and prompts the user for the next input.

---

## 🚀 Getting Started

### Prerequisites
* Webcam & Microphone access.
* Modern Web Browser (Chrome recommended).

### Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/keep-in-touch.git](https://github.com/your-username/keep-in-touch.git)
    ```
2.  **Install Dependencies:**
    ```bash
    npm install  # or pip install -r requirements.txt
    ```
3.  **Run the App:**
    ```bash
    npm start
    ```

---

## 📈 Engineering Highlights

* **Low Latency:** Optimized gesture recognition for near-instant response times.
* **Dynamic Feedback:** Seamless transition between visual gestures and voice commands.
* **Inclusive Design:** Built with accessibility-first principles.

---

## ✉️ Contact
RACHELI
Project Link: [https://github.com/your-username/keep-in-touch](https://github.com/your-username/keep-in-touch)
