---
layout: times-table-flyer
title: Print Flyer | Times Table Unleashed
permalink: /times-table-unleashed/flyer/
main_nav: false
---

<main class="flyer-sheet" aria-label="Two print-ready Times Table Unleashed flyers">
  {% for copy in (1..2) %}
  <article class="flyer">
    <div class="flyer-content">
      <div class="flyer-brand"><img src="/assets/times-table-unleashed/app-icon.png" alt=""><span>TIMES TABLE<br><span>UNLEASHED</span></span></div>
      <div class="phone"><img src="/assets/times-table-unleashed/home.png" alt="Times Table Unleashed app home screen"></div>
      <div class="fact-chip">3 × 4</div>
      <h1>Make multiplication <strong>click.</strong></h1>
      <p class="tagline">A cheerful game that helps learners build multiplication confidence—one fact, one streak, one small win at a time.</p>
      <ul class="benefits">
        <li><b>Play &amp; practice</b>Quick game rounds make it easy to get started.</li>
        <li><b>Learn with hints</b>Friendly prompts help facts stick.</li>
        <li><b>Celebrate growth</b>Build streaks and stars across themed levels.</li>
        <li><b>See progress</b>Use the Mastery Map and Teacher Report.</li>
      </ul>
      <div class="flyer-bottom">
        <div><h2>Coming soon to the App Store</h2><p>For iPhone and iPad · No ads · No tracking · No accounts<br>Learn more: ryanguill.com/times-table-unleashed</p></div>
        <div class="qr-placeholder" aria-label="QR code placeholder"><span>APP STORE<br>QR SOON</span></div>
      </div>
    </div>
    <span class="cut-label">CUT HERE</span>
  </article>
  {% endfor %}
</main>
