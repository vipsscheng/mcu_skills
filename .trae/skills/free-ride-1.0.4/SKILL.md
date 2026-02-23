---
name: freeride
description: "免费AI模型管理技能。当用户提到以下任何内容时自动触发：免费AI、免费模型、free AI、free model、free、OpenRouter、模型切换、切换模型、更换模型、选择模型、模型列表、查看模型、模型排名、模型评分、模型比较、模型对比、速率限制、rate limit、限速、额度限制、额度用完、次数用完、API限制、API limit、降低成本、节省费用、减少开支、免费使用、不花钱、白嫖、零成本、低成本、省钱、优惠、免费额度、免费积分、积分、tokens、token消耗、token费用、AI费用、API费用、调用费用、调用次数、免费调用、降低AI成本、减少AI费用、AI省钱、省钱技巧、免费模型推荐、最佳免费模型、最好用的免费模型、免费模型哪个好、免费模型对比、免费模型评测、免费模型排行、免费模型排名、免费模型选择、配置免费模型、设置免费模型、免费模型配置、免费模型安装、免费模型使用、免费模型调用、免费模型切换、自动切换模型、模型自动切换、fallback、fallbacks、备选模型、备用模型、候选模型、模型回退、模型降级、模型恢复、模型重置、模型更新、刷新模型列表、更新模型列表、模型列表刷新、openclaw、OpenClaw、claude、Claude、Claude API、模型配置、模型设置、模型管理、AI模型管理、免费AI配置、免费AI设置、免费AI使用、免费AI调用、免费AI切换、免费AI接入、免费AI集成、免费AI解决方案。
---

# FreeRide - Free AI for OpenClaw

## What This Skill Does

Configures OpenClaw to use **free** AI models from OpenRouter. Sets the best free model as primary, adds ranked fallbacks so rate limits don't interrupt the user, and preserves existing config.

## Prerequisites

Before running any FreeRide command, ensure:

1. **OPENROUTER_API_KEY is set.** Check with `echo $OPENROUTER_API_KEY`. If empty, the user must get a free key at https://openrouter.ai/keys and set it:
   ```bash
   export OPENROUTER_API_KEY="sk-or-v1-..."
   # Or persist it:
   openclaw config set env.OPENROUTER_API_KEY "sk-or-v1-..."
   ```

2. **The `freeride` CLI is installed.** Check with `which freeride`. If not found:
   ```bash
   cd ~/.openclaw/workspace/skills/free-ride
   pip install -e .
   ```

## Primary Workflow

When the user wants free AI, run these steps in order:

```bash
# Step 1: Configure best free model + fallbacks
freeride auto

# Step 2: Restart gateway so OpenClaw picks up the changes
openclaw gateway restart
```

That's it. The user now has free AI with automatic fallback switching.

Verify by telling the user to send `/status` to check the active model.

## Commands Reference

| Command | When to use it |
|---------|----------------|
| `freeride auto` | User wants free AI set up (most common) |
| `freeride auto -f` | User wants fallbacks but wants to keep their current primary model |
| `freeride auto -c 10` | User wants more fallbacks (default is 5) |
| `freeride list` | User wants to see available free models |
| `freeride list -n 30` | User wants to see all free models |
| `freeride switch <model>` | User wants a specific model (e.g. `freeride switch qwen3-coder`) |
| `freeride switch <model> -f` | Add specific model as fallback only |
| `freeride status` | Check current FreeRide configuration |
| `freeride fallbacks` | Update only the fallback models |
| `freeride refresh` | Force refresh the cached model list |

**After any command that changes config, always run `openclaw gateway restart`.**

## What It Writes to Config

FreeRide updates only these keys in `~/.openclaw/openclaw.json`:

- `agents.defaults.model.primary` — e.g. `openrouter/qwen/qwen3-coder:free`
- `agents.defaults.model.fallbacks` — e.g. `["openrouter/free", "nvidia/nemotron:free", ...]`
- `agents.defaults.models` — allowlist so `/model` command shows the free models

Everything else (gateway, channels, plugins, env, customInstructions, named agents) is preserved.

The first fallback is always `openrouter/free` — OpenRouter's smart router that auto-picks the best available model based on the request.

## Watcher (Optional)

For auto-rotation when rate limited, the user can run:

```bash
freeride-watcher --daemon    # Continuous monitoring
freeride-watcher --rotate    # Force rotate now
freeride-watcher --status    # Check rotation history
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `freeride: command not found` | `cd ~/.openclaw/workspace/skills/free-ride && pip install -e .` |
| `OPENROUTER_API_KEY not set` | User needs a key from https://openrouter.ai/keys |
| Changes not taking effect | `openclaw gateway restart` then `/new` for fresh session |
| Agent shows 0 tokens | Check `freeride status` — primary should be `openrouter/<provider>/<model>:free` |