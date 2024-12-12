const form = document.getElementById("slotForm");
const slot1 = document.getElementById("slot1");
const slot2 = document.getElementById("slot2");
const slot3 = document.getElementById("slot3");
const result = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const lines = parseInt(document.getElementById("lines").value);
  const bet = parseInt(document.getElementById("bet").value);

  const response = await fetch("/spin", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ lines, bet }),
  });

  const data = await response.json();
  if (response.ok) {
    const [s1, s2, s3] = data.slots.map((col) => col.join("|"));
    slot1.textContent = s1;
    slot2.textContent = s2;
    slot3.textContent = s3;

    result.textContent = `Winnings: $${data.winnings}, Lines: ${data.winning_lines.join(", ")}`;
  } else {
    result.textContent = data.error || "An error occurred.";
  }
});
