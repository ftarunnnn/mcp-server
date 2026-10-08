"""
CLI Entry Point for AI Developer MCP Server supporting stdio and SSE transports.
"""

import sys
import click
import uvicorn
from starlette.responses import HTMLResponse
from ai_developer_mcp.server import mcp, logger
from ai_developer_mcp.config import config


@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport protocol to use: 'stdio' (default) for Claude/Cursor, 'sse' for HTTP streaming."
)
@click.option(
    "--host",
    default="0.0.0.0",
    help="Host address for SSE transport (default: 0.0.0.0)."
)
@click.option(
    "--port",
    default=8000,
    type=int,
    help="Port for SSE transport (default: 8000)."
)
def main(transport: str, host: str, port: int):
    """
    Launch the AI Developer MCP Server.
    """
    logger.info(f"Starting AI Developer MCP Server via {transport.upper()} transport...")
    
    if transport == "stdio":
        mcp.run(transport="stdio")
    elif transport == "sse":
        app = mcp.sse_app()
        
        # Add root HTML dashboard endpoint for web browser visits
        async def root_dashboard(request):
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{config.server_name}</title>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                        background: #0f172a;
                        color: #f8fafc;
                        margin: 0;
                        padding: 40px 20px;
                        display: flex;
                        justify-content: center;
                    }}
                    .container {{
                        max-width: 800px;
                        width: 100%;
                        background: #1e293b;
                        padding: 32px;
                        border-radius: 16px;
                        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                        border: 1px solid #334155;
                    }}
                    h1 {{ color: #38bdf8; font-size: 2rem; margin-top: 0; }}
                    .badge {{
                        background: #10b981;
                        color: #064e3b;
                        padding: 4px 12px;
                        border-radius: 9999px;
                        font-weight: bold;
                        font-size: 0.875rem;
                    }}
                    .card {{
                        background: #0f172a;
                        padding: 16px;
                        border-radius: 8px;
                        margin-top: 16px;
                        border: 1px solid #334155;
                    }}
                    code {{
                        background: #334155;
                        color: #f43f5e;
                        padding: 2px 6px;
                        border-radius: 4px;
                        font-family: monospace;
                    }}
                    ul {{ padding-left: 20px; }}
                    li {{ margin-bottom: 8px; }}
                    a {{ color: #38bdf8; text-decoration: none; }}
                    a:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h1>🚀 {config.server_name}</h1>
                        <span class="badge">ONLINE</span>
                    </div>
                    <p>Model Context Protocol (MCP) Server is active and listening for AI client connections.</p>
                    
                    <div class="card">
                        <h3>🔗 Connection Details</h3>
                        <p><b>SSE Endpoint:</b> <code>http://{host}:{port}/sse</code></p>
                        <p><b>Protocol:</b> JSON-RPC 2.0 over Server-Sent Events</p>
                        <p><b>Workspace Root:</b> <code>{config.workspace_dir.absolute()}</code></p>
                    </div>

                    <div class="card">
                        <h3>🛠️ Available Capabilities</h3>
                        <ul>
                            <li><b>Tools:</b> <code>search_code</code>, <code>analyze_code</code>, <code>generate_tests</code>, <code>run_command</code>, <code>search_documentation</code>, <code>git_operations</code>, <code>github_get_repo_info</code>, <code>github_search_issues</code></li>
                            <li><b>Resources:</b> <code>project://files/{{path}}</code>, <code>docs://architecture</code>, <code>config://server-status</code></li>
                            <li><b>Prompts:</b> <code>code_review</code>, <code>debugging</code>, <code>architecture_review</code></li>
                        </ul>
                    </div>

                    <div class="card">
                        <h3>💡 How to Use</h3>
                        <p>Configure this server in Claude Desktop, Cursor, or any MCP-compatible AI client using:</p>
                        <pre style="background:#1e293b; padding:12px; border-radius:6px; overflow-x:auto;"><code>http://localhost:{port}/sse</code></pre>
                    </div>
                </div>
            </body>
            </html>
            """
            return HTMLResponse(content=html_content)

        app.add_route("/", root_dashboard, methods=["GET"])

        logger.info(f"Serving SSE transport and web dashboard on http://{host}:{port}")
        uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
