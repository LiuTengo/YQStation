# Agent Guidance for YQStation

Purpose
-------
This file gives concise, actionable guidance for AI coding agents working in this repository. Follow the "link, don't embed" principle: point to existing docs and code rather than copying large sections.

Quick start (development)
-------------------------
- Backend (Python)

  ```bash
  cd backend/app
  .venv\Scripts\Activate.ps1   # Windows PowerShell
  pip install -r ../requirements.txt  # if present
  uvicorn main:app --reload
  ```

- Frontend (Vite / TypeScript)

  ```bash
  cd frontend/YQStationApp
  npm install
  npm run dev
  ```

Key files and locations
-----------------------
- Backend entry: [backend/app/main.py](backend/app/main.py#L1)
- API models: [backend/app/requestModel.py](backend/app/requestModel.py#L1)
- Repositories: [backend/app/repository/ExcelRepository.py](backend/app/repository/ExcelRepository.py#L1)
- Sample data: [backend/app/data/excel/20260518_测试活动/lecture_info.json](backend/app/data/excel/20260518_测试活动/lecture_info.json)
- Frontend entry: [frontend/YQStationApp/src/main.ts](frontend/YQStationApp/src/main.ts#L1)
- Frontend README: [frontend/YQStationApp/README.md](frontend/YQStationApp/README.md#L1)

Conventions and notes
---------------------
- Python virtual environment: `.venv` is used in workspace root (activate before running backend).
- Frontend uses Vite + TypeScript inside `frontend/YQStationApp`.
- Keep changes minimal and well-tested. Open a PR for behavioral changes.
- Do not commit secrets or large binary data. Ask before modifying production data files under `backend/app/data`.

Agent behavior guidance
----------------------
- Prefer creating or updating `AGENTS.md` over adding `.github/copilot-instructions.md` unless requested.
- When in doubt, run the dev servers locally before changing APIs or UI.
- Link to docs rather than embedding them; include file links for any code references you use.

Further actions
---------------
If you'd like, I can also:
- add a `.github/copilot-instructions.md` with a short agent checklist
- create focused agent skills for `backend` and `frontend` workflows

Please tell me which follow-up you'd prefer.
