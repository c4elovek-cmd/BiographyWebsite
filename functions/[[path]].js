// Catch-all: сначала отдаём статический файл (next()), а для несуществующих
// путей ищем короткую ссылку в KV (переезжает из Worker secure-shortener).
export async function onRequest(context) {
  const { request, env, params, next } = context;

  const response = await next();
  if (response.status !== 404) {
    return response;
  }

  const url = new URL(request.url);
  if (url.pathname.startsWith("/api/")) {
    return new Response(JSON.stringify({ error: "Not found" }), {
      status: 404,
      headers: { "Content-Type": "application/json" }
    });
  }

  const path = (Array.isArray(params.path) ? params.path.join("/") : params.path) || "";
  if (!path) {
    return response;
  }

  const rawData = await env.LINKS.get(path);
  if (!rawData) {
    return response;
  }

  let targetUrl = rawData;
  let pwd = null;
  let isOneTime = false;

  try {
    const parsed = JSON.parse(rawData);
    if (parsed && parsed.u) {
      targetUrl = parsed.u;
      pwd = parsed.p;
      isOneTime = parsed.o;
    }
  } catch (e) {}

  if (pwd) {
    const authHeader = request.headers.get("Authorization");
    if (!authHeader) {
      return new Response("Требуется пароль", {
        status: 401,
        headers: { "WWW-Authenticate": 'Basic realm="Введи пароль для перехода"' }
      });
    }
    const base64 = authHeader.split(" ")[1];
    const providedPwd = atob(base64).split(":")[1];

    if (providedPwd !== pwd) {
      return new Response("Неверный пароль", {
        status: 401,
        headers: { "WWW-Authenticate": 'Basic realm="Неверно. Попробуй еще раз"' }
      });
    }
  }

  if (isOneTime) {
    await env.LINKS.delete(path);
  }

  return Response.redirect(targetUrl, 301);
}
