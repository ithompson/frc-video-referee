# FRC Video Referee - Development Setup

This document outlines how to set up and run the FRC Video Referee web application.

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the development server:**
   ```bash
   frc-video-referee --reload
   ```

3. **Access the application:**
   - Open your browser to `http://localhost:8000`
   - Default credentials: `admin` / `password`

## Project Structure

```
frc-video-referee/
├── src/frc_video_referee/
│   ├── __init__.py          # Main entry point
│   ├── server.py            # FastAPI server implementation
│   └── static/              # Static files (copied during build, gitignored)
├── static/                  # Development static files (source of truth)
│   ├── index.html           # Main HTML page
│   ├── style.css           # CSS styles
│   └── app.js              # JavaScript client
├── dev_utils.py            # Development utilities
├── pyproject.toml          # Project configuration
└── README.md
```

## Static Files Management

The project uses a single source of truth for static files:

- **Source**: `static/` directory (tracked in git)
- **Development**: Server automatically serves from `static/` directory
- **Production**: Files are copied to package during build

### Development Workflow

1. **Edit static files** in the `static/` directory
2. **Run server** with `frc-video-referee --reload`
3. **Changes are served immediately** (no copying needed)

### Building for Distribution

When building the package, static files are automatically embedded into the package:

```bash
# Build package (embeds static/ into frc_video_referee/static/ in the wheel)
uv build
```

The static files are included using Hatch's `force-include` mechanism, which embeds them directly into the package rather than installing them to global shared directories.

## Features

### ✅ Implemented

- **FastAPI Server**: Modern async web framework
- **Static File Serving**: Serves from `static/` directory in development
- **WebSocket Support**: Real-time bidirectional communication
- **Basic Authentication**: Simple password-based auth for API endpoints
- **Development/Production Modes**: Different static file locations
- **Command Line Interface**: Easy server startup with options

### 🔄 Architecture

- **Development Mode**: Static files served from workspace `static/` directory
- **Production Mode**: Static files served from installed package
- **Authentication**: All API endpoints require basic auth except static files
- **WebSocket**: Available at `/ws` for real-time updates

### 📋 Planned (SvelteKit Frontend)

- Modern frontend framework
- Component-based architecture
- Build process for static assets
- Hot module replacement in development

## API Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/` | GET | No | Serves main application page |
| `/static/*` | GET | No | Static file serving |
| `/api/status` | GET | Yes | Server status information |
| `/ws` | WebSocket | No | Real-time communication |

## Development

### Running the Server

```bash
# Basic server
frc-video-referee

# With custom host/port
frc-video-referee --host 0.0.0.0 --port 3000

# With auto-reload for development
frc-video-referee --reload
```

### Authentication

The server uses HTTP Basic Authentication for API endpoints:
- **Username**: `admin`
- **Password**: `password`

> **Note**: In production, move credentials to environment variables.

### WebSocket Usage

The WebSocket endpoint at `/ws` provides real-time communication:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => {
    console.log('Received:', event.data);
};
ws.send('Hello, server!');
```

## Future: SvelteKit Integration

The frontend will be implemented using SvelteKit, which will:

1. **Build Process**: Generate optimized static assets
2. **Development Server**: Hot module replacement and fast refresh
3. **Component System**: Reusable UI components
4. **Routing**: Client-side routing with server-side rendering options
5. **Asset Pipeline**: Automatic optimization and bundling

### Planned Directory Structure

```
frontend/                   # SvelteKit application
├── src/
│   ├── app.html           # HTML shell
│   ├── routes/            # SvelteKit routes
│   └── lib/               # Shared components
├── static/                # SvelteKit static assets
├── build/                 # Built assets (goes to main static/)
└── svelte.config.js       # SvelteKit configuration
```

## Security Notes

- Static files are served without authentication
- All API endpoints require basic authentication
- WebSocket connections are currently unauthenticated
- Consider implementing JWT tokens for production use

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure dependencies are installed with `uv sync`
2. **Port Already in Use**: Use a different port with `--port 3001`
3. **WebSocket Connection Issues**: Check firewall settings and proxy configuration

### Development Tips

- Use `--reload` flag for automatic server restarts during development
- Check the browser console for WebSocket connection status
- API endpoints can be tested with tools like `curl` or Postman

## License

This project is licensed under the terms specified in the LICENSE file.
