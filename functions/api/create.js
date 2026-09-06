// POST /api/create — создание короткой ссылки (Pages Functions, KV: LINKS)
export async function onRequestPost(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  try {
    const { targetUrl, password, expireTtl, isOneTime, customLength, useSpecialChars } = await request.json();

    const generateSecureCode = (length, useSpecial) => {
      let charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
      if (useSpecial) charset += "-_.~@!*'()";

      let safeLength = parseInt(length) || 12;
      if (safeLength < 3) safeLength = 3;
      if (safeLength > 50) safeLength = 50;

      let result = "";
      const randomValues = new Uint32Array(safeLength);
      crypto.getRandomValues(randomValues);
      for (let i = 0; i < safeLength; i++) result += charset[randomValues[i] % charset.length];
      return result;
    };

    let secureCode;
    let isUnique = false;
    let attempts = 0;

    while (!isUnique && attempts < 5) {
      secureCode = generateSecureCode(customLength, useSpecialChars);
      const existing = await env.LINKS.get(secureCode);
      if (!existing) isUnique = true;
      attempts++;
    }

    if (!isUnique) {
      return new Response(JSON.stringify({ error: "Не удалось сгенерировать уникальный код. Увеличьте длину ссылки." }), { status: 500 });
    }

    const linkData = JSON.stringify({
      u: targetUrl,
      p: password || null,
      o: isOneTime || false
    });

    let kvOptions = {};
    if (expireTtl) kvOptions.expirationTtl = parseInt(expireTtl);

    await env.LINKS.put(secureCode, linkData, kvOptions);

    return new Response(JSON.stringify({ shortUrl: `https://${url.hostname}/${secureCode}` }), {
      headers: { "Content-Type": "application/json" }
    });
  } catch (e) {
    return new Response("Error", { status: 400 });
  }
}

export async function onRequest(context) {
  return new Response(JSON.stringify({ error: "Use POST" }), { status: 405 });
}
