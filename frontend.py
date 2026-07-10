<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes" />
    <title>Enterprise AI Assistant</title>
    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
    <style>
        /* ─── RESET & ROOT ─── */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg: #F2F4F9;
            --surface: #FFFFFF;
            --surface-2: #F8F9FD;
            --border: #E4E7F0;
            --border-strong: #CDD2E0;
            --text-primary: #0F111B;
            --text-secondary: #4A4F5E;
            --text-tertiary: #888D9E;
            --accent: #4A44E6;
            --accent-hover: #3A34C9;
            --accent-soft: #EDECFD;
            --accent-glow: rgba(74, 68, 230, 0.15);
            --spark: #F5A524;
            --spark-soft: #FEF5E6;
            --success: #17B26A;
            --success-soft: #ECFDF3;
            --danger: #E4483F;
            --danger-soft: #FEF3F2;
            --radius-xl: 24px;
            --radius-lg: 18px;
            --radius-md: 12px;
            --radius-sm: 9px;
            --shadow-xs: 0 1px 2px rgba(15, 17, 27, 0.04);
            --shadow-sm: 0 2px 8px rgba(15, 17, 27, 0.06);
            --shadow-md: 0 8px 30px rgba(15, 17, 27, 0.08);
            --shadow-lg: 0 20px 50px rgba(15, 17, 27, 0.12);
            --shadow-xl: 0 32px 64px rgba(15, 17, 27, 0.16);
            --transition: 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        html,
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg);
            color: var(--text-primary);
            height: 100%;
            overflow: hidden;
        }

        /* ─── APP SHELL ─── */
        #app {
            display: flex;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
            background:
                radial-gradient(circle at 80% 10%, rgba(74, 68, 230, 0.05), transparent 50%),
                radial-gradient(circle at 20% 90%, rgba(245, 165, 36, 0.04), transparent 40%),
                var(--bg);
        }

        /* ─── SIDEBAR ─── */
        #sidebar {
            width: 320px;
            min-width: 320px;
            height: 100%;
            background: var(--surface);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            transition: transform var(--transition), margin var(--transition);
            z-index: 100;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-sm);
        }

        #sidebar.closed {
            margin-left: -320px;
            transform: translateX(-320px);
        }

        #sidebar-inner {
            padding: 24px 20px 28px 20px;
            overflow-y: auto;
            flex: 1;
            scrollbar-width: thin;
            scrollbar-color: var(--border) transparent;
        }
        #sidebar-inner::-webkit-scrollbar {
            width: 4px;
        }
        #sidebar-inner::-webkit-scrollbar-thumb {
            background: var(--border-strong);
            border-radius: 99px;
        }

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 4px;
        }
        .sidebar-brand-icon {
            width: 38px;
            height: 38px;
            border-radius: 11px;
            background: linear-gradient(135deg, var(--accent), #7A6EF0);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(74, 68, 230, 0.25);
            flex-shrink: 0;
        }
        .sidebar-brand-icon svg {
            width: 20px;
            height: 20px;
            fill: white;
        }
        .sidebar-brand-text {
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            line-height: 1.2;
        }
        .sidebar-brand-sub {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.6rem;
            font-weight: 600;
            color: var(--text-tertiary);
            letter-spacing: 0.03em;
            margin-top: 2px;
        }

        .sidebar-divider {
            border: none;
            border-top: 1px solid var(--border);
            margin: 18px 0 20px 0;
        }

        .sidebar-section-title {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-tertiary);
            margin-bottom: 12px;
        }

        /* Field cards */
        .field-card {
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 14px 16px 16px 16px;
            margin-bottom: 14px;
            transition: border var(--transition);
        }
        .field-card:focus-within {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }
        .field-card-label {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 8px;
        }
        .field-card-label i {
            color: var(--accent);
            font-size: 0.9rem;
            width: 18px;
            text-align: center;
        }
        .field-card-hint {
            font-size: 0.7rem;
            color: var(--text-tertiary);
            margin-top: 8px;
            line-height: 1.4;
        }

        /* Custom select */
        .custom-select {
            width: 100%;
            padding: 9px 12px;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border-strong);
            background: var(--surface);
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            font-weight: 500;
            color: var(--text-primary);
            outline: none;
            transition: border var(--transition), box-shadow var(--transition);
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%23888D9E' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 12px center;
            cursor: pointer;
        }
        .custom-select:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }

        .model-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            font-weight: 700;
            color: var(--accent);
            background: var(--accent-soft);
            padding: 4px 12px;
            border-radius: 99px;
            margin-top: 8px;
            max-width: 100%;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .model-badge i {
            font-size: 0.5rem;
        }

        /* Toggle switch */
        .toggle-wrap {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 4px 0;
        }
        .toggle-track {
            width: 44px;
            height: 26px;
            border-radius: 99px;
            background: var(--border-strong);
            cursor: pointer;
            position: relative;
            flex-shrink: 0;
            transition: background var(--transition);
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.06);
        }
        .toggle-track.active {
            background: var(--accent);
        }
        .toggle-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: white;
            position: absolute;
            top: 3px;
            left: 3px;
            transition: transform var(--transition);
            box-shadow: var(--shadow-xs);
        }
        .toggle-track.active .toggle-thumb {
            transform: translateX(18px);
        }
        .toggle-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-primary);
            user-select: none;
        }

        /* Expander */
        .custom-expander {
            border: 1px solid var(--border-strong);
            border-radius: var(--radius-sm);
            overflow: hidden;
            margin-top: 4px;
        }
        .custom-expander summary {
            padding: 10px 14px;
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--text-primary);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            background: var(--surface-2);
            user-select: none;
            list-style: none;
        }
        .custom-expander summary::-webkit-details-marker {
            display: none;
        }
        .custom-expander summary i {
            font-size: 0.75rem;
            color: var(--text-tertiary);
            transition: transform var(--transition);
        }
        .custom-expander[open] summary i {
            transform: rotate(90deg);
        }
        .custom-expander textarea {
            width: 100%;
            padding: 12px 14px;
            border: none;
            border-top: 1px solid var(--border);
            font-family: 'Inter', sans-serif;
            font-size: 0.82rem;
            color: var(--text-primary);
            background: var(--surface);
            resize: vertical;
            min-height: 80px;
            outline: none;
            line-height: 1.5;
        }
        .custom-expander textarea:focus {
            background: var(--surface);
        }

        /* Sidebar button */
        .sidebar-btn {
            width: 100%;
            padding: 11px 16px;
            border-radius: var(--radius-sm);
            border: 1.5px solid var(--danger);
            background: var(--danger-soft);
            color: var(--danger);
            font-family: 'Inter', sans-serif;
            font-size: 0.82rem;
            font-weight: 700;
            cursor: pointer;
            transition: all var(--transition);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        .sidebar-btn:hover {
            background: var(--danger);
            color: white;
            border-color: var(--danger);
        }
        .sidebar-btn i {
            font-size: 0.9rem;
        }

        .sidebar-footer {
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid var(--border);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.6rem;
            color: var(--text-tertiary);
            letter-spacing: 0.02em;
            line-height: 1.6;
        }

        /* ─── MAIN CHAT AREA ─── */
        #main {
            flex: 1;
            display: flex;
            flex-direction: column;
            height: 100%;
            min-width: 0;
            position: relative;
        }

        /* ─── HEADER ─── */
        #header {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 14px 20px 10px 20px;
            background: transparent;
            flex-shrink: 0;
            flex-wrap: wrap;
            row-gap: 8px;
        }

        .hamburger {
            width: 40px;
            height: 40px;
            border-radius: var(--radius-sm);
            border: none;
            background: var(--surface);
            box-shadow: var(--shadow-sm);
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 4px;
            transition: all var(--transition);
            flex-shrink: 0;
            border: 1px solid var(--border);
        }
        .hamburger:hover {
            box-shadow: var(--shadow-md);
            border-color: var(--accent);
        }
        .hamburger span {
            display: block;
            width: 18px;
            height: 2px;
            background: var(--text-primary);
            border-radius: 99px;
            transition: all var(--transition);
        }
        .hamburger.active span:nth-child(1) {
            transform: translateY(6px) rotate(45deg);
        }
        .hamburger.active span:nth-child(2) {
            opacity: 0;
        }
        .hamburger.active span:nth-child(3) {
            transform: translateY(-6px) rotate(-45deg);
        }

        .header-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            flex: 1;
            min-width: 0;
        }
        .header-brand-icon {
            width: 34px;
            height: 34px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--accent), #7A6EF0);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            box-shadow: 0 3px 10px rgba(74, 68, 230, 0.2);
        }
        .header-brand-icon svg {
            width: 18px;
            height: 18px;
            fill: white;
        }
        .header-brand-title {
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .header-brand-sub {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.55rem;
            font-weight: 600;
            color: var(--text-tertiary);
            letter-spacing: 0.04em;
            display: block;
            margin-top: 1px;
        }

        .header-status {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 5px 14px 5px 12px;
            background: var(--success-soft);
            border: 1px solid #CDF2DE;
            border-radius: 99px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.58rem;
            font-weight: 700;
            color: #0A8A50;
            letter-spacing: 0.04em;
            white-space: nowrap;
            flex-shrink: 0;
        }
        .header-status .dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 0 3px rgba(23, 178, 106, 0.15);
            animation: pulse-dot 2s infinite;
        }
        @keyframes pulse-dot {
            0%,
            100% {
                opacity: 1;
                transform: scale(1);
            }
            50% {
                opacity: 0.6;
                transform: scale(0.85);
            }
        }

        /* ─── MESSAGES AREA ─── */
        #messages {
            flex: 1;
            overflow-y: auto;
            padding: 4px 20px 20px 20px;
            scroll-behavior: smooth;
            display: flex;
            flex-direction: column;
            gap: 6px;
            scrollbar-width: thin;
            scrollbar-color: var(--border) transparent;
        }
        #messages::-webkit-scrollbar {
            width: 4px;
        }
        #messages::-webkit-scrollbar-thumb {
            background: var(--border-strong);
            border-radius: 99px;
        }

        /* ─── EMPTY STATE ─── */
        .empty-state {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
            min-height: 300px;
        }
        .empty-state-icon {
            width: 72px;
            height: 72px;
            border-radius: 20px;
            background: linear-gradient(135deg, var(--accent), #7A6EF0);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 30px rgba(74, 68, 230, 0.2);
            margin-bottom: 20px;
        }
        .empty-state-icon svg {
            width: 30px;
            height: 30px;
            fill: white;
        }
        .empty-state-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 6px;
        }
        .empty-state-desc {
            font-size: 0.88rem;
            color: var(--text-tertiary);
            max-width: 340px;
            line-height: 1.6;
        }

        /* ─── MESSAGE BUBBLES ─── */
        .msg-wrap {
            display: flex;
            gap: 12px;
            max-width: 88%;
            animation: msg-in 0.3s ease;
        }
        .msg-wrap.user {
            align-self: flex-end;
            flex-direction: row-reverse;
        }
        .msg-wrap.assistant {
            align-self: flex-start;
        }

        @keyframes msg-in {
            0% {
                opacity: 0;
                transform: translateY(12px) scale(0.97);
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .msg-avatar {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 15px;
            box-shadow: var(--shadow-xs);
            margin-top: 2px;
        }
        .msg-avatar.user {
            background: var(--surface);
            border: 1px solid var(--border);
            color: var(--text-secondary);
        }
        .msg-avatar.assistant {
            background: linear-gradient(135deg, var(--accent), #7A6EF0);
            color: white;
            box-shadow: 0 3px 10px rgba(74, 68, 230, 0.2);
        }

        .msg-bubble {
            padding: 12px 16px;
            border-radius: var(--radius-lg);
            font-size: 0.92rem;
            line-height: 1.6;
            word-break: break-word;
            box-shadow: var(--shadow-xs);
            position: relative;
            min-width: 40px;
        }
        .msg-wrap.user .msg-bubble {
            background: var(--accent);
            color: white;
            border-bottom-right-radius: 4px;
        }
        .msg-wrap.assistant .msg-bubble {
            background: var(--surface);
            border: 1px solid var(--border);
            color: var(--text-primary);
            border-bottom-left-radius: 4px;
        }

        .msg-bubble code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            background: rgba(0, 0, 0, 0.06);
            padding: 2px 6px;
            border-radius: 4px;
            color: #C0255C;
        }
        .msg-wrap.user .msg-bubble code {
            background: rgba(255, 255, 255, 0.15);
            color: #FFD7E0;
        }
        .msg-bubble pre {
            background: #0F111B;
            border-radius: var(--radius-sm);
            padding: 12px 14px;
            overflow-x: auto;
            margin: 8px 0 4px 0;
            font-size: 0.78rem;
        }
        .msg-bubble pre code {
            background: transparent !important;
            color: #E6E8F0 !important;
            padding: 0;
            font-size: 0.78rem;
        }
        .msg-bubble p {
            margin: 0 0 6px 0;
        }
        .msg-bubble p:last-child {
            margin-bottom: 0;
        }
        .msg-bubble ul,
        .msg-bubble ol {
            margin: 4px 0 6px 16px;
            padding-left: 4px;
        }
        .msg-bubble li {
            margin-bottom: 2px;
        }

        .msg-meta {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 6px;
            font-size: 0.6rem;
            color: var(--text-tertiary);
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.02em;
            opacity: 0.7;
        }
        .msg-wrap.user .msg-meta {
            justify-content: flex-end;
            color: rgba(255, 255, 255, 0.6);
        }
        .msg-wrap.assistant .msg-meta {
            color: var(--text-tertiary);
        }

        /* ─── TYPING INDICATOR ─── */
        .typing-wrap {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 0 4px 0;
            animation: msg-in 0.3s ease;
        }
        .typing-dots {
            display: flex;
            gap: 4px;
            padding: 10px 16px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            border-bottom-left-radius: 4px;
            box-shadow: var(--shadow-xs);
        }
        .typing-dots span {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--text-tertiary);
            display: inline-block;
            animation: typing-bounce 1.4s infinite ease-in-out both;
        }
        .typing-dots span:nth-child(1) {
            animation-delay: 0s;
        }
        .typing-dots span:nth-child(2) {
            animation-delay: 0.2s;
        }
        .typing-dots span:nth-child(3) {
            animation-delay: 0.4s;
        }
        @keyframes typing-bounce {
            0%,
            80%,
            100% {
                transform: scale(0.6);
                opacity: 0.4;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }

        /* ─── CHAT INPUT ─── */
        #input-area {
            padding: 10px 20px 16px 20px;
            flex-shrink: 0;
            background: transparent;
        }
        .input-wrap {
            display: flex;
            gap: 10px;
            align-items: flex-end;
            background: var(--surface);
            border: 1.5px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 6px 6px 6px 16px;
            box-shadow: var(--shadow-md);
            transition: border var(--transition), box-shadow var(--transition);
        }
        .input-wrap:focus-within {
            border-color: var(--accent);
            box-shadow: var(--shadow-lg), 0 0 0 4px var(--accent-glow);
        }
        .input-wrap textarea {
            flex: 1;
            border: none;
            outline: none;
            resize: none;
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: var(--text-primary);
            background: transparent;
            padding: 8px 0;
            min-height: 24px;
            max-height: 120px;
            line-height: 1.5;
        }
        .input-wrap textarea::placeholder {
            color: var(--text-tertiary);
        }
        .input-wrap .send-btn {
            width: 42px;
            height: 42px;
            border-radius: 50%;
            border: none;
            background: linear-gradient(135deg, var(--accent), #7A6EF0);
            color: white;
            font-size: 1rem;
            cursor: pointer;
            transition: all var(--transition);
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 14px rgba(74, 68, 230, 0.25);
        }
        .input-wrap .send-btn:hover {
            transform: scale(1.04);
            box-shadow: 0 6px 20px rgba(74, 68, 230, 0.35);
        }
        .input-wrap .send-btn:active {
            transform: scale(0.95);
        }
        .input-wrap .send-btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        /* ─── TOAST / ALERT ─── */
        .toast {
            padding: 12px 16px;
            border-radius: var(--radius-md);
            font-size: 0.85rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
            animation: msg-in 0.3s ease;
            border: 1px solid transparent;
        }
        .toast.error {
            background: var(--danger-soft);
            border-color: #FDD8D5;
            color: var(--danger);
        }
        .toast.error i {
            color: var(--danger);
        }
        .toast.success {
            background: var(--success-soft);
            border-color: #CDF2DE;
            color: var(--success);
        }
        .toast i {
            font-size: 1rem;
        }

        /* ─── SIDEBAR OVERLAY (mobile) ─── */
        #sidebar-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(15, 17, 27, 0.3);
            backdrop-filter: blur(4px);
            z-index: 99;
            opacity: 0;
            transition: opacity var(--transition);
            pointer-events: none;
        }
        #sidebar-overlay.visible {
            opacity: 1;
            pointer-events: auto;
        }

        /* ─── RESPONSIVE ─── */
        @media (max-width: 768px) {
            #sidebar {
                position: fixed;
                top: 0;
                left: 0;
                height: 100%;
                width: 300px;
                min-width: 300px;
                transform: translateX(-300px);
                border-radius: 0 20px 20px 0;
                box-shadow: var(--shadow-xl);
                transition: transform var(--transition);
            }
            #sidebar.open {
                transform: translateX(0);
            }
            #sidebar.closed {
                transform: translateX(-300px);
                margin-left: 0;
            }
            #sidebar-overlay.visible {
                display: block;
            }

            #header {
                padding: 12px 14px 8px 14px;
                gap: 10px;
            }
            .header-brand-title {
                font-size: 0.95rem;
            }
            .header-brand-sub {
                font-size: 0.5rem;
            }
            .header-status {
                font-size: 0.5rem;
                padding: 4px 10px 4px 8px;
            }
            .header-status .dot {
                width: 5px;
                height: 5px;
            }

            #messages {
                padding: 4px 14px 14px 14px;
                gap: 4px;
            }
            .msg-wrap {
                max-width: 94%;
            }
            .msg-bubble {
                font-size: 0.88rem;
                padding: 10px 14px;
            }
            .msg-avatar {
                width: 30px;
                height: 30px;
                font-size: 13px;
            }

            #input-area {
                padding: 8px 14px 14px 14px;
            }
            .input-wrap {
                padding: 4px 4px 4px 12px;
                border-radius: 16px;
            }
            .input-wrap textarea {
                font-size: 0.88rem;
                padding: 6px 0;
            }
            .input-wrap .send-btn {
                width: 38px;
                height: 38px;
                font-size: 0.9rem;
            }

            .empty-state-icon {
                width: 60px;
                height: 60px;
            }
            .empty-state-icon svg {
                width: 24px;
                height: 24px;
            }
            .empty-state-title {
                font-size: 1rem;
            }
            .empty-state-desc {
                font-size: 0.82rem;
            }
        }

        @media (max-width: 400px) {
            #sidebar {
                width: 280px;
                min-width: 280px;
                transform: translateX(-280px);
            }
            #sidebar.open {
                transform: translateX(0);
            }
            #sidebar.closed {
                transform: translateX(-280px);
            }
            .header-brand-title {
                font-size: 0.85rem;
            }
            .header-status {
                font-size: 0.45rem;
                padding: 3px 8px 3px 6px;
            }
            .msg-bubble {
                font-size: 0.84rem;
                padding: 8px 12px;
            }
            .msg-wrap {
                max-width: 96%;
            }
            .input-wrap textarea {
                font-size: 0.84rem;
            }
            .sidebar-brand-text {
                font-size: 1rem;
            }
        }

        /* ─── SCROLLBAR STYLING ─── */
        ::-webkit-scrollbar {
            width: 4px;
            height: 4px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: var(--border-strong);
            border-radius: 99px;
        }

        /* ─── UTILITY ─── */
        .hidden {
            display: none !important;
        }
        .flex-1 {
            flex: 1;
        }
        .mt-1 {
            margin-top: 6px;
        }
        .mb-1 {
            margin-bottom: 6px;
        }
        .gap-1 {
            gap: 6px;
        }
        .text-center {
            text-align: center;
        }
    </style>
</head>
<body>

    <div id="app">
        <!-- SIDEBAR OVERLAY (mobile) -->
        <div id="sidebar-overlay"></div>

        <!-- SIDEBAR -->
        <aside id="sidebar">
            <div id="sidebar-inner">
                <!-- Brand -->
                <div class="sidebar-brand">
                    <div class="sidebar-brand-icon">
                        <svg viewBox="0 0 24 24"><path d="M13 2L4 14H11L10 22L20 9H13L13 2Z"/></svg>
                    </div>
                    <div>
                        <div class="sidebar-brand-text">Control Panel</div>
                        <div class="sidebar-brand-sub">GROQ · LANGGRAPH</div>
                    </div>
                </div>
                <hr class="sidebar-divider" />

                <!-- Brain Engine -->
                <div class="field-card">
                    <div class="field-card-label"><i class="fas fa-brain"></i> Brain Engine</div>
                    <select id="modelSelect" class="custom-select">
                        <option value="llama-3.3-70b-versatile">llama-3.3-70b-versatile</option>
                        <option value="mixtral-8x7b-32768">mixtral-8x7b-32768</option>
                    </select>
                    <div class="model-badge"><i class="fas fa-circle"></i> <span id="modelBadgeText">llama-3.3-70b-versatile</span></div>
                </div>

                <!-- Live Web Search -->
                <div class="field-card">
                    <div class="field-card-label"><i class="fas fa-globe"></i> Live Web Search</div>
                    <div class="toggle-wrap">
                        <div id="searchToggle" class="toggle-track active" role="button" tabindex="0">
                            <div class="toggle-thumb"></div>
                        </div>
                        <span class="toggle-label" id="searchLabel">Enabled</span>
                    </div>
                    <div class="field-card-hint">When on, the assistant can pull in current information from the web.</div>
                </div>

                <!-- Advanced Settings -->
                <div class="field-card">
                    <div class="field-card-label"><i class="fas fa-sliders-h"></i> Advanced Settings</div>
                    <details class="custom-expander">
                        <summary><i class="fas fa-chevron-right"></i> System Prompt</summary>
                        <textarea id="systemPrompt" placeholder="Enter system prompt...">You are a highly intelligent, concise AI assistant.</textarea>
                    </details>
                </div>

                <!-- Clear Button -->
                <button id="clearBtn" class="sidebar-btn"><i class="fas fa-trash-alt"></i> Clear Chat History</button>

                <div class="sidebar-footer">
                    v1.0.0 · FastAPI backend<br />127.0.0.1:8000
                </div>
            </div>
        </aside>

        <!-- MAIN -->
        <main id="main">
            <!-- HEADER -->
            <header id="header">
                <button id="hamburgerBtn" class="hamburger" aria-label="Toggle sidebar">
                    <span></span><span></span><span></span>
                </button>
                <div class="header-brand">
                    <div class="header-brand-icon">
                        <svg viewBox="0 0 24 24"><path d="M13 2L4 14H11L10 22L20 9H13L13 2Z"/></svg>
                    </div>
                    <div>
                        <div class="header-brand-title">Enterprise AI</div>
                        <span class="header-brand-sub">⚡ GROQ LPUs</span>
                    </div>
                </div>
                <div class="header-status">
                    <span class="dot"></span>
                    <span>ONLINE</span>
                </div>
            </header>

            <!-- MESSAGES -->
            <div id="messages">
                <!-- Empty state (shown by default, hidden when messages exist) -->
                <div id="emptyState" class="empty-state">
                    <div class="empty-state-icon">
                        <svg viewBox="0 0 24 24"><path d="M13 2L4 14H11L10 22L20 9H13L13 2Z"/></svg>
                    </div>
                    <p class="empty-state-title">Start a conversation</p>
                    <p class="empty-state-desc">Ask a question, paste something to analyze, or describe a task — the assistant is ready.</p>
                </div>
                <!-- Messages will be inserted here by JS -->
            </div>

            <!-- INPUT -->
            <div id="input-area">
                <div class="input-wrap">
                    <textarea id="chatInput" rows="1" placeholder="Type your message here..." autocomplete="off"></textarea>
                    <button id="sendBtn" class="send-btn" aria-label="Send message">
                        <i class="fas fa-arrow-up"></i>
                    </button>
                </div>
            </div>
        </main>
    </div>

    <script>
        // ─── DOM REFS ───
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        const hamburger = document.getElementById('hamburgerBtn');
        const messagesEl = document.getElementById('messages');
        const emptyState = document.getElementById('emptyState');
        const chatInput = document.getElementById('chatInput');
        const sendBtn = document.getElementById('sendBtn');
        const modelSelect = document.getElementById('modelSelect');
        const modelBadgeText = document.getElementById('modelBadgeText');
        const searchToggle = document.getElementById('searchToggle');
        const searchLabel = document.getElementById('searchLabel');
        const systemPrompt = document.getElementById('systemPrompt');
        const clearBtn = document.getElementById('clearBtn');

        // ─── STATE ───
        let messages = [];
        let isSidebarOpen = false;
        let isSearchEnabled = true;
        let isProcessing = false;
        let currentModel = modelSelect.value;

        // ─── SIDEBAR TOGGLE ───
        function toggleSidebar(open) {
            const shouldOpen = open !== undefined ? open : !isSidebarOpen;
            isSidebarOpen = shouldOpen;

            if (window.innerWidth <= 768) {
                sidebar.classList.toggle('open', shouldOpen);
                sidebar.classList.toggle('closed', !shouldOpen);
                overlay.classList.toggle('visible', shouldOpen);
                hamburger.classList.toggle('active', shouldOpen);
            } else {
                sidebar.classList.toggle('closed', !shouldOpen);
                hamburger.classList.toggle('active', shouldOpen);
            }
        }

        hamburger.addEventListener('click', () => toggleSidebar());
        overlay.addEventListener('click', () => toggleSidebar(false));

        // Close sidebar on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && isSidebarOpen && window.innerWidth <= 768) {
                toggleSidebar(false);
            }
        });

        // Handle resize: reset sidebar state
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                if (window.innerWidth > 768) {
                    sidebar.classList.remove('open');
                    overlay.classList.remove('visible');
                    // On desktop, sidebar should be open by default
                    if (!isSidebarOpen) {
                        sidebar.classList.add('closed');
                    } else {
                        sidebar.classList.remove('closed');
                    }
                } else {
                    sidebar.classList.remove('closed');
                    if (!isSidebarOpen) {
                        sidebar.classList.remove('open');
                        overlay.classList.remove('visible');
                        hamburger.classList.remove('active');
                    }
                }
            }, 150);
        });

        // ─── MODEL SELECT ───
        modelSelect.addEventListener('change', () => {
            currentModel = modelSelect.value;
            modelBadgeText.textContent = currentModel;
        });

        // ─── SEARCH TOGGLE ───
        searchToggle.addEventListener('click', () => {
            isSearchEnabled = !isSearchEnabled;
            searchToggle.classList.toggle('active', isSearchEnabled);
            searchLabel.textContent = isSearchEnabled ? 'Enabled' : 'Disabled';
        });
        searchToggle.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                searchToggle.click();
            }
        });

        // ─── CLEAR CHAT ───
        clearBtn.addEventListener('click', () => {
            messages = [];
            renderMessages();
            // Also clear any error toast
            const toast = messagesEl.querySelector('.toast');
            if (toast) toast.remove();
        });

        // ─── RENDER MESSAGES ───
        function renderMessages() {
            // Remove all message nodes but keep empty state and any toast
            const toKeep = [];
            const children = messagesEl.children;
            for (let i = 0; i < children.length; i++) {
                if (children[i].id === 'emptyState' || children[i].classList.contains('toast')) {
                    toKeep.push(children[i]);
                }
            }
            // Clear all
            while (messagesEl.firstChild) {
                messagesEl.removeChild(messagesEl.firstChild);
            }
            // Re-add kept elements
            toKeep.forEach(el => messagesEl.appendChild(el));

            // Show/hide empty state
            if (messages.length === 0) {
                emptyState.style.display = 'flex';
            } else {
                emptyState.style.display = 'none';
            }

            // Render messages
            messages.forEach((msg, idx) => {
                const wrap = document.createElement('div');
                wrap.className = `msg-wrap ${msg.role}`;
                wrap.dataset.index = idx;

                // Avatar
                const avatar = document.createElement('div');
                avatar.className = `msg-avatar ${msg.role}`;
                avatar.innerHTML = msg.role === 'user' ?
                    '<i class="fas fa-user"></i>' :
                    '<i class="fas fa-bolt"></i>';
                wrap.appendChild(avatar);

                // Bubble
                const bubble = document.createElement('div');
                bubble.className = 'msg-bubble';
                // Use innerHTML for markdown-like support (simple)
                bubble.innerHTML = formatMessage(msg.content);
                wrap.appendChild(bubble);

                // Meta (time)
                const meta = document.createElement('div');
                meta.className = 'msg-meta';
                const now = new Date();
                const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                meta.innerHTML = `<span>${timeStr}</span>`;
                if (msg.role === 'assistant') {
                    meta.innerHTML += ` · <span>${currentModel}</span>`;
                }
                wrap.appendChild(meta);

                messagesEl.appendChild(wrap);
            });

            // Scroll to bottom
            messagesEl.scrollTop = messagesEl.scrollHeight;
        }

        // ─── FORMAT MESSAGE (simple markdown-like) ───
        function formatMessage(text) {
            // Escape HTML
            let html = text
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;');

            // Code blocks
            html = html.replace(/```([\s\S]*?)```/g, (_, code) => {
                return `<pre><code>${code.trim()}</code></pre>`;
            });

            // Inline code
            html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

            // Bold
            html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

            // Italic
            html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

            // Line breaks
            html = html.replace(/\n/g, '<br>');

            return html;
        }

        // ─── ADD MESSAGE ───
        function addMessage(role, content) {
            messages.push({ role, content });
            renderMessages();
        }

        // ─── SHOW TOAST ───
        function showToast(message, type = 'error') {
            // Remove existing toast
            const existing = messagesEl.querySelector('.toast');
            if (existing) existing.remove();

            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            const icon = type === 'error' ? 'fa-exclamation-circle' : 'fa-check-circle';
            toast.innerHTML = `<i class="fas ${icon}"></i> ${message}`;
            // Insert after empty state or at top
            const ref = messagesEl.querySelector('#emptyState');
            if (ref && messages.length === 0) {
                messagesEl.insertBefore(toast, ref);
            } else {
                messagesEl.prepend(toast);
            }
            // Auto-remove after 6s
            setTimeout(() => {
                if (toast.parentNode) toast.remove();
            }, 6000);
        }

        // ─── SHOW TYPING ───
        function showTyping() {
            const wrap = document.createElement('div');
            wrap.className = 'typing-wrap';
            wrap.id = 'typingIndicator';
            const avatar = document.createElement('div');
            avatar.className = 'msg-avatar assistant';
            avatar.innerHTML = '<i class="fas fa-bolt"></i>';
            wrap.appendChild(avatar);
            const dots = document.createElement('div');
            dots.className = 'typing-dots';
            dots.innerHTML = '<span></span><span></span><span></span>';
            wrap.appendChild(dots);
            messagesEl.appendChild(wrap);
            messagesEl.scrollTop = messagesEl.scrollHeight;
        }

        function hideTyping() {
            const el = document.getElementById('typingIndicator');
            if (el) el.remove();
        }

        // ─── SEND MESSAGE ───
        async function sendMessage() {
            const text = chatInput.value.trim();
            if (!text || isProcessing) return;

            // Clear input
            chatInput.value = '';
            chatInput.style.height = 'auto';

            // Add user message
            addMessage('user', text);

            // Disable input
            isProcessing = true;
            sendBtn.disabled = true;
            chatInput.disabled = true;

            // Show typing indicator
            showTyping();

            // Get system prompt
            const sysPrompt = systemPrompt.value.trim() || 'You are a highly intelligent, concise AI assistant.';

            // Build payload
            const payload = {
                messages: messages.filter(m => m.role === 'user').map(m => m.content),
                system_prompt: sysPrompt,
                model_name: currentModel,
                allow_search: isSearchEnabled
            };

            try {
                const resp = await fetch('https://enterprise-langgraph-chatbot.onrender.com/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                hideTyping();

                if (!resp.ok) {
                    let errMsg = `Backend error (${resp.status})`;
                    try {
                        const errData = await resp.json();
                        errMsg = errData.detail || errMsg;
                    } catch (_) {}
                    showToast(`🚨 ${errMsg}`, 'error');
                    return;
                }

                const data = await resp.json();
                const reply = data.response || 'No response from backend.';
                addMessage('assistant', reply);

            } catch (err) {
                hideTyping();
                if (err instanceof TypeError && err.message.includes('fetch')) {
                    showToast('🔌 Connection Error: Make sure your FastAPI backend is running!', 'error');
                } else {
                    showToast(`⚠️ Error: ${err.message}`, 'error');
                }
            } finally {
                isProcessing = false;
                sendBtn.disabled = false;
                chatInput.disabled = false;
                chatInput.focus();
            }
        }

        // ─── EVENT LISTENERS ───
        sendBtn.addEventListener('click', sendMessage);

        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Auto-resize textarea
        chatInput.addEventListener('input', () => {
            chatInput.style.height = 'auto';
            chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
        });

        // ─── INIT ───
        // On desktop, sidebar starts open
        if (window.innerWidth > 768) {
            isSidebarOpen = true;
            sidebar.classList.remove('closed');
        } else {
            isSidebarOpen = false;
            sidebar.classList.add('closed');
            sidebar.classList.remove('open');
        }

        // Focus input on load
        setTimeout(() => chatInput.focus(), 300);

        // ─── DEMO: Add a welcome message (optional) ───
        // Uncomment to add a welcome message on load
        // addMessage('assistant', '👋 Hello! I\'m your Enterprise AI Assistant. How can I help you today?');

        console.log('🚀 Enterprise AI Assistant ready');
        console.log(`📦 Model: ${currentModel}`);
        console.log(`🔍 Search: ${isSearchEnabled ? 'ON' : 'OFF'}`);
    </script>
</body>
</html>
