/* global chrome */

export const sendCommandToGmail = (command, value = null) => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (!tabs[0]?.id) return;

    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: (cmd, val) => {

        // 1. פתיחת מייל חדש
        if (cmd === "compose") {
          document.querySelector('.T-I.T-I-KE')?.click();
        }

        // 2. שליחת מייל
        if (cmd === "send") {
          document.dispatchEvent(
            new KeyboardEvent("keydown", { key: "Enter", ctrlKey: true })
          );
        }

        // 3. פתיחת מייל ראשון
        if (cmd === "open_first") {
          document.querySelector("tr.zA")?.click();
        }

        // 4. מעבר בין מיילים
        if (cmd === "next") {
          document.dispatchEvent(new KeyboardEvent("keydown", { key: "j" }));
        }

        if (cmd === "prev") {
          document.dispatchEvent(new KeyboardEvent("keydown", { key: "k" }));
        }

      },
      args: [command, value]
    });
  });
};