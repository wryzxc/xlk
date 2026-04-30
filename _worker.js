// EdgeOne Pages Worker 入口文件
// 用于处理静态资源请求和路由转发

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // 静态资源缓存策略
    if (url.pathname.startsWith('/static/')) {
      const response = await env.ASSETS.fetch(request);
      const headers = new Headers(response.headers);
      
      // CSS/JS 文件长期缓存
      if (url.pathname.match(/\.(css|js)$/)) {
        headers.set('Cache-Control', 'public, max-age=31536000, immutable');
      }
      // 图片/字体文件缓存
      if (url.pathname.match(/\.(png|jpg|jpeg|gif|webp|svg|woff|woff2)$/)) {
        headers.set('Cache-Control', 'public, max-age=2592000');
      }
      
      return new Response(response.body, {
        status: response.status,
        headers: headers
      });
    }
    
    // 安全响应头
    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    headers.set('X-Content-Type-Options', 'nosniff');
    headers.set('X-Frame-Options', 'SAMEORIGIN');
    headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    headers.set('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
    
    return new Response(response.body, {
      status: response.status,
      headers: headers
    });
  }
};
