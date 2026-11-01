# User Stories

## Personas
- **Requester**: non-technical employee from another department. Never sees specs, code or terminals. Wants a working tool for their problem.
- **Platform Developer**: engineer who maintains the builder and adds providers (agent frameworks, tracing, object store, sandbox).
- **Platform Admin**: operates the deployment, config, and keeps usage and failures under control.

Priority: **P0** = v1 happy path, **P1** = v1 if time allows, **P2** = later.

---

## Epic 1: Describe what I need (chat)
| ID | Story | Acceptance criteria | Pri |
|----|-------|---------------------|-----|
| US-1.1 | As a Requester, I want to type my need in plain words so that I don't have to know technical terms. | Given an empty project, when I submit free text, then the system accepts it and starts the clarify step. No technical fields are required. | P0 |
| US-1.2 | As a Requester, I want to be asked a few simple multiple-choice questions so that the app matches what I meant. | Given a vague request, then I see 3-5 questions with 2-4 options plus "Other" and a "not sure, you decide" choice. Max 2 rounds, then the system proceeds with stated assumptions. | P0 |
| US-1.3 | As a Requester, I want to see a plain-language summary of what will be built so that I can confirm before waiting for a build. | Summary lists screens and features in non-technical bullets (no spec jargon). I can press Build or Change. | P0 |
| US-1.4 | As a Requester, I want sample prompts/examples so that I know what to ask for. | Empty-state shows 3+ clickable examples (leave tracker, inventory list, feedback form, "clean up my spreadsheet"). | P1 |

## Epic 2: Bring my own data
| ID | Story | Acceptance criteria | Pri |
|----|-------|---------------------|-----|
| US-2.1 | As a Requester, I want to upload a data file (CSV or Excel) alongside my request so that the app works on my real data. | Drag-and-drop or file picker in the chat. Accepts `.csv` and `.xlsx`, with a clear friendly error for unsupported types, empty files, or files over the size limit. | P0 |
| US-2.2 | As a Requester, I want the system to understand my data so that I don't have to describe columns. | After upload, I see a plain-language preview ("I found 1,240 rows with Name, Department, Hire date, Salary") with the first rows; column types are inferred and I can correct them in simple dropdowns. | P0 |
| US-2.3 | As a Requester, I want to say what the app should do with the data (e.g. "show total salary by department", "flag duplicates", "let me edit rows") so that the app is built around the data. | The data profile (columns, types, sample rows) is fed to the clarify and spec steps, so the generated data model matches the uploaded columns, and the request is reflected in the build summary. | P0 |
| US-2.4 | As a Requester, I want my uploaded data to be loaded into the built app so that I can test it right away. | After build, the app's database is pre-loaded with the uploaded rows. The preview shows them, and the feature I asked for works on them. | P0 |
| US-2.5 | As a Requester, I want to upload a new or updated file later so that I can retest with fresh data. | "Replace data" re-imports into the active version, with a choice to replace or add rows, after confirmation. | P1 |
| US-2.6 | As a Requester, I want to upload several files (e.g. employees and departments) so that the app can relate them. | Multiple files become separate tables; the system asks one plain-language question when a link between them is ambiguous. | P1 |
| US-2.7 | As a Requester, I want to download results from the test app (export to CSV/Excel) so that I can check the outcome in familiar tools. | Generated apps expose an Export button for each table/report. | P1 |
| US-2.8 | As a Requester, I want to be told how my data is handled so that I feel safe uploading it. | The upload dialog states that data stays on this server and is only used for this project. Delete data on project delete. | P0 |
| US-2.9 | As a Requester, I want messy data handled gracefully so that a bad row doesn't ruin the import. | Import reports "1,238 rows loaded, 2 skipped" with a downloadable list of skipped rows and reasons. | P1 |

## Epic 3: Build the app (hidden SDD pipeline)
| ID | Story | Acceptance criteria | Pri |
|----|-------|---------------------|-----|
| US-3.1 | As a Requester, I want the system to turn my request (and data profile) into specs automatically so that the result is consistent and traceable. | Spec, plan and tasks files are generated and stored per version, and are never shown in the Requester UI. | P0 |
| US-3.2 | As a Requester, I want to see friendly progress while it builds so that I know it is working. | Progress streams as plain steps ("Creating the form...", "Loading your data...") via SSE; no stack traces or file names. | P0 |
| US-3.3 | As a Requester, I want the build to check itself so that I don't receive a broken app. | Given a finished build, the app boots, every route in the spec responds OK, and imported row counts match the upload. On failure the system retries up to 3 times automatically. | P0 |
| US-3.4 | As a Requester, I want a clear, kind message if the build ultimately fails so that I know what to do next. | After retries are exhausted I see a plain-language message and options: "Try again" or "Simplify my request". Technical detail is only in logs. | P0 |
| US-3.5 | As a Requester, I want to cancel a running build so that I don't wait for the wrong thing. | Cancel stops agent and sandbox processes and keeps the previous version intact. | P1 |

## Epic 4: Test the app
| ID | Story | Acceptance criteria | Pri |
|----|-------|---------------------|-----|
| US-4.1 | As a Requester, I want to try the built app inside the builder so that I can verify it solves my issue. | When the build completes, the running app is shown in an iframe via the preview proxy. I can use the feature on my data, and add or edit a record. | P0 |
| US-4.2 | As a Requester, I want to reset the test data so that I can retest from a clean state. | "Reset data" restores the originally uploaded dataset (or empty if none) after confirmation. | P0 |
| US-4.3 | As a Requester, I want to restart the app if it hangs so that I'm not stuck. | "Restart" relaunches the sandbox process and the preview recovers within ~10s. | P1 |
| US-4.4 | As a Requester, I want my test app to still be there tomorrow so that I can continue later. | Reopening a project restores its latest version and data, and relaunches the preview on demand. | P0 |

## Epic 5: Change it in plain words
| ID | Story | Acceptance criteria | Pri |
|----|-------|---------------------|-----|
| US-5.1 | As a Requester, I want to ask for changes in plain words so that I don't start over. | Given a built app, when I type "add a due date column" or "also group by region", then specs are updated by diff, the delta is built, and a new version appears. | P0 |
| US-5.2 | As a Requester, I want old versions kept so that a bad change is never a disaster. | Each build creates `v{n}`. The version list shows time and a plain-language summary of each. | P0 |
| US-5.3 | As a Requester, I want to roll back to an earlier version so that I can undo a change I don't like. | Rollback makes the chosen version the active one and relaunches preview; later versions remain available. | P0 |
| US-5.4 | As a Requester, I want my existing data to survive a change when possible so that testing isn't lost. | Additive changes (new field) keep rows; destructive changes warn me before proceeding. | P2 |

## Epic 6: Projects
| ID | Story | Acceptance criteria | Pri |
|----|-------|---------------------|-----|
| US-6.1 | As a Requester, I want a list of my projects so that I can manage several tools. | List shows name, status (building/ready/failed), last updated. I can create, rename and delete (with confirmation; deleting also removes uploaded data). | P0 |
| US-6.2 | As a Requester, I want to share a finished app with colleagues so that they can use it. | Out of scope for v1. Tracked for later (needs auth and hosting). | P2 |

## Epic 7: Platform extensibility (Platform Developer)
| ID | Story | Acceptance criteria | Pri |
|----|-------|---------------------|-----|
| US-7.1 | As a Platform Developer, I want to switch the agent framework via config so that I can use a different one without touching feature code. | Setting `AGENT=<name>` changes the runtime through `core/factory.get_agent()`. No imports of concrete providers exist under `backend/app/`. | P0 |
| US-7.2 | As a Platform Developer, I want to add a new provider by extending `base.py` and registering it so that onboarding is quick. | A new class extends the port ABC, is registered in `registry.py`, and passes the shared contract tests for that port. | P0 |
| US-7.3 | As a Platform Developer, I want the same pattern for llm, prompts, tracing, object store and sandbox so that infrastructure is consistent. | Each of the 5 ports has a `base.py`, at least one real implementation, and a fake for tests. Uploaded files are stored via the object store port. | P0 |
| US-7.4 | As a Platform Developer, I want traces of every pipeline step so that I can debug bad generations. | Each build emits a trace with profile, clarify, spec, code, import and verify spans, including prompts, outputs and timing, via the configured Tracer. | P1 |
| US-7.5 | As a Platform Developer, I want to edit prompts and spec templates without code changes so that I can tune quality. | Prompts are read from `backend/prompts/` through the PromptStore, and a change takes effect on the next build. | P0 |

## Epic 8: Safety and operations (Platform Admin)
| ID | Story | Acceptance criteria | Pri |
|----|-------|---------------------|-----|
| US-8.1 | As a Platform Admin, I want generated code isolated so that a bad app can't harm the host. | Agent is limited to its workspace and a tool allowlist; apps bind to 127.0.0.1 and have no access to builder secrets. | P0 |
| US-8.2 | As a Platform Admin, I want orphan processes cleaned up so that the machine doesn't fill with stale apps. | On builder shutdown and on idle timeout, sandbox process trees are killed (including on Windows). | P0 |
| US-8.3 | As a Platform Admin, I want limits (build time, retries, disk, upload size and row count) so that cost and resources stay bounded. | Configurable caps are enforced and surface as a friendly failure to the Requester. | P1 |
| US-8.4 | As a Platform Admin, I want secrets only in env config so that nothing sensitive lands in code or workspaces. | Startup fails fast with a clear message when a required secret is missing. | P0 |
| US-8.5 | As a Platform Admin, I want uploads validated and kept away from the model unnecessarily so that data is protected. | Files are type/size checked and never executed (CSV formula cells neutralized on export). Only the schema plus a few sample rows go to the LLM, never the full dataset (configurable). Uploaded files are stored through the object store and removed on project delete. | P0 |

---

## Walking skeleton (first end-to-end slice)
US-1.1, 1.2, 1.3 -> 2.1, 2.2, 2.3, 2.4 -> 3.1, 3.2, 3.3 -> 4.1 -> 5.1, 5.2, 5.3, plus 7.1-7.3 and 8.1, 8.5. Everything else layers on top.
