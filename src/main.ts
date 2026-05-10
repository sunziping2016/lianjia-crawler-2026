class Main {
  public readonly container: HTMLElement;
  public readonly server: string;

  private backoff: number;

  constructor(server: string) {
    const div = document.createElement("div");
    div.style.position = "fixed";
    div.style.top = "50px";
    div.style.width = "200px";
    div.style.right = "60px";
    div.style.zIndex = "1500";
    div.style.backgroundColor = "white";
    div.style.border = "1px solid #666";
    div.style.cursor = "pointer";
    div.style.padding = "0.5em";
    div.style.borderRadius = "0.5em";
    this.container = div;
    this.server = server;
    this.backoff = 10;
  }

  async start() {
    while (true) {
      try {
        await this.doStart();
      } catch (e) {
        this.setStatus("Error: " + e);
        console.error(e);
      } finally {
        this.setStatus("Error: disconnected");
      }
      this.backoff = Math.min(this.backoff * 2, 60 * 1000);
      await new Promise((resolve) => setTimeout(resolve, this.backoff));
    }
  }

  private setStatus(status: string) {
    this.container.textContent = `${status}`;
  }

  private async doStart() {
    const { promise, resolve, reject } = Promise.withResolvers<void>();
    const ws = new WebSocket(this.server);
    this.setStatus("Connecting");
    ws.onopen = () => {
      this.setStatus("Connected");
      this.backoff = 10;
    };
    ws.onmessage = () => {};
    ws.onclose = () => {
      resolve();
    };
    ws.onerror = (event) => {
      reject(event);
    };
    return promise;
  }
}

(async () => {
  const main = new Main("ws://localhost:8080/ws");
  document.body.appendChild(main.container);
  await main.start();
})();
