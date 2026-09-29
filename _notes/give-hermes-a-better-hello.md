---
title: "Give Hermes a better hello"
description: "The giant new-chat splash in Hermes Desktop is text, not an image. A small local plugin can make it yours."
date: 2026-09-25
tags: [hermes, desktop]
image:
  path: /assets/hermes-custom-hello.png
  alt: "Illustrated light-mode Hermes desktop with a winged envelope and the splash text DESIRE IS PROTOCOL."
---

I went looking for the giant new-chat splash as an image. There isn't one. Hermes Desktop renders it as text, which means I can give it my own hello without rebuilding the app.

![Illustration of a light-themed Hermes new-chat window with a little winged envelope and the words DESIRE IS PROTOCOL.](/assets/hermes-custom-hello.png)

I wanted mine to say **DESIRE IS PROTOCOL**. The illustration is a playful mockup; the plugin below changes the actual wordmark and hides the stock prompt beneath it.

Create `~/.hermes/desktop-plugins/custom-intro/plugin.js`:

```js
const TEXT = 'DESIRE IS PROTOCOL'
const INTRO = '[data-slot="aui_intro"]'
const originals = new WeakMap()

function leaves(wordmark) {
  return [...wordmark.querySelectorAll('span')].filter(span => span.children.length === 0)
}

function apply() {
  for (const intro of document.querySelectorAll(INTRO)) {
    const wordmark = intro.querySelector('p.wordmark')
    if (!wordmark) continue

    if (!originals.has(wordmark)) {
      originals.set(wordmark, {
        label: wordmark.getAttribute('aria-label'),
        spans: leaves(wordmark).map(span => [span, span.textContent]),
      })
    }

    intro.dataset.customIntro = ''
    wordmark.setAttribute('aria-label', TEXT)
    for (const span of leaves(wordmark)) {
      if (span.textContent !== TEXT) span.textContent = TEXT
    }
  }
}

export default {
  id: 'custom-intro',
  name: 'Custom Intro',
  register(ctx) {
    const style = document.createElement('style')
    style.textContent = `${INTRO}[data-custom-intro] > div > p:not(.wordmark) { display: none !important; }`
    document.head.append(style)

    const observer = new MutationObserver(records => {
      const containsIntro = node => node.nodeType === 1 &&
        (node.matches(INTRO) || node.querySelector(INTRO))
      if (records.some(({ target, addedNodes }) =>
        (target.nodeType === 1 ? target : target.parentElement)?.closest(INTRO) ||
        [...addedNodes].some(containsIntro)
      )) apply()
    })
    observer.observe(document.documentElement, {
      childList: true,
      subtree: true,
      characterData: true,
    })
    apply()

    ctx.onDispose(() => {
      observer.disconnect()
      style.remove()
      for (const intro of document.querySelectorAll(INTRO)) {
        const wordmark = intro.querySelector('p.wordmark')
        const original = wordmark && originals.get(wordmark)
        if (!original) continue
        if (original.label === null) wordmark.removeAttribute('aria-label')
        else wordmark.setAttribute('aria-label', original.label)
        for (const [span, text] of original.spans) span.textContent = text
        delete intro.dataset.customIntro
      }
    })
  },
}
```

The two visible and sizing spans both need the new text, or the fitted wordmark can size itself against the old one. The observer catches a fresh intro when React remounts the new-chat screen; the cleanup puts the original text back if the plugin is disabled.

Hermes watches the desktop-plugin folder, so a save should hot-reload without an app rebuild. If nothing appears, check that **Intro Splash** is enabled in Appearance and that **Custom Intro** is enabled in Settings → Plugins. The `data-slot` and wordmark selectors target today's desktop markup, so revisit them if a future app update changes the splash.

The nice part is the location: the plugin lives in your Hermes home, outside the application checkout. Change `TEXT` to whatever you want. The hello is yours.
