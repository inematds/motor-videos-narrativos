#!/usr/bin/env python3
"""Motor de direção para vídeos narrativos em pt-BR.

Gera um plano de produção e um pacote de prompts. Ele não copia a referência:
aprende princípios e escolhe combinações novas usando um histórico local.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "engine_config.json"
HISTORY_PATH = ROOT / "history.json"


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write("\n")


def rng_for(seed: int, label: str) -> random.Random:
    digest = hashlib.sha256(f"{seed}:{label}".encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def choose(items: list[dict[str, Any]], rng: random.Random, blocked: Iterable[str], key: str = "id") -> dict[str, Any]:
    blocked = set(blocked)
    available = [item for item in items if item.get(key) not in blocked]
    return rng.choice(available or items)


def choose_many(items: list[dict[str, Any]], rng: random.Random, count: int, blocked: Iterable[str], key: str = "id") -> list[dict[str, Any]]:
    blocked = set(blocked)
    preferred = [item for item in items if item.get(key) not in blocked]
    pool = preferred if len(preferred) >= count else items
    return rng.sample(pool, min(count, len(pool)))


def clip(text: str, max_words: int = 8) -> str:
    words = text.split()
    return " ".join(words[:max_words]) + ("…" if len(words) > max_words else "")


def fmt_time(seconds: float) -> str:
    whole = int(seconds)
    return f"{whole // 60:02d}:{whole % 60:02d}"


def make_windows(duration: float, beat_ids: list[str]) -> list[tuple[str, float, float]]:
    # Hook e CTA recebem espaço suficiente; o restante acompanha a narrativa.
    if len(beat_ids) == 6:
        weights = [0.13, 0.16, 0.19, 0.19, 0.21, 0.12]
    elif len(beat_ids) == 5:
        weights = [0.15, 0.20, 0.23, 0.25, 0.17]
    else:
        weights = [1.0 / len(beat_ids)] * len(beat_ids)
    total = sum(weights)
    cursor = 0.0
    result = []
    for beat_id, weight in zip(beat_ids, weights):
        start = cursor
        cursor += duration * weight / total
        result.append((beat_id, start, cursor))
    result[-1] = (result[-1][0], result[-1][1], duration)
    return result


def camera_sequence(cameras: list[str], rng: random.Random, count: int) -> list[str]:
    if not cameras:
        return []
    shuffled = cameras[:]
    rng.shuffle(shuffled)
    result: list[str] = []
    while len(result) < count:
        for move in shuffled:
            if result and move == result[-1]:
                continue
            result.append(move)
            if len(result) == count:
                break
        rng.shuffle(shuffled)
    return result


def beat_goal(beat_id: str, topic: str, archetype: str) -> str:
    goals = {
        "hook": f"Abrir uma tensão concreta sobre {topic} e prometer uma resposta sem entregar tudo.",
        "origin": f"Apresentar o ponto de partida de {topic} e por que ele importa.",
        "rise": f"Mostrar a mudança, mecanismo ou expansão que fez {topic} ganhar peso.",
        "crisis": f"Introduzir a contradição, custo, risco ou virada escondida em {topic}.",
        "legacy": f"Conectar {topic} a uma consequência atual, humana ou cultural.",
        "cta": "Fechar com uma ação única e coerente com o objetivo do vídeo.",
        "myth": f"Nomear a crença comum sobre {topic} sem ridicularizar quem acredita nela.",
        "evidence": f"Apresentar a evidência ou mecanismo que muda a leitura de {topic}.",
        "turn": f"Entregar a revelação que reorganiza o que o espectador acabou de ouvir.",
        "meaning": f"Explicar por que a revelação sobre {topic} é relevante hoje.",
        "problem": f"Mostrar o problema real que {topic} ajuda a entender.",
        "mechanism": f"Visualizar passo a passo como o mecanismo de {topic} funciona.",
        "proof": f"Dar um caso, número ou demonstração que sustenta a explicação.",
        "solution": f"Apresentar a solução, decisão ou aprendizado prático ligado a {topic}.",
        "consequence": f"Começar pela consequência mais surpreendente relacionada a {topic}.",
        "clue": f"Voltar a uma pista visual ou verbal que explica a consequência.",
        "present": f"Trazer a consequência para o presente e tornar a ideia acionável.",
        "destination": f"Mostrar o destino, resultado ou pergunta final antes de voltar ao início.",
        "place_one": f"Estabelecer o primeiro lugar ou momento necessário para entender {topic}.",
        "place_two": f"Mudar de espaço ou tempo para revelar uma conexão em {topic}.",
        "place_three": f"Chegar ao terceiro ponto, onde a história de {topic} ganha significado.",
        "connection": f"Unir os pontos e explicar o fio comum de {topic}.",
        "object_hook": f"Usar um objeto ligado a {topic} como testemunha silenciosa da história.",
        "past": f"Reconstituir o passado do objeto sem transformar o vídeo em catálogo.",
        "owner": f"Mostrar quem usou, guardou ou transformou o objeto relacionado a {topic}.",
    }
    return goals.get(beat_id, f"Desenvolver a etapa {beat_id} da narrativa sobre {topic} usando o arquétipo {archetype}.")


def visual_direction(grammar_ids: list[str], beat_id: str, topic: str) -> str:
    grammar = grammar_ids[0]
    if beat_id == "hook":
        return f"Começar com uma imagem ou símbolo de alto contraste ligado a {topic}; esconder parte da informação e revelar um detalhe no primeiro segundo. Gramática: {grammar}."
    if beat_id == "cta":
        return f"Apresentar a ação final relacionada a {topic} em composição limpa, com espaço negativo para texto e um hold de leitura. Gramática: {grammar}."
    return f"Mostrar {topic} em uma composição que torne visível a ideia narrada; alternar escala e detalhe. Gramática visual dominante: {grammar}."


def text_direction(beat_id: str, topic: str, rng: random.Random) -> str:
    variants = {
        "hook": ["uma pergunta curta", "uma data ou número", "uma consequência em 3–6 palavras"],
        "cta": ["uma ação direta", "uma pergunta para comentário", "um convite curto"],
    }
    choices = variants.get(beat_id, ["nome, lugar, data ou palavra-chave", "um número ou contraste", "um título curto sincronizado com a fala"])
    return f"Exibir {rng.choice(choices)} sobre {topic}; no máximo 8 palavras por entrada, alto contraste e margem segura."


def build_plan(args: argparse.Namespace, config: dict[str, Any], history: dict[str, Any]) -> dict[str, Any]:
    seed = args.seed if args.seed is not None else random.SystemRandom().randint(1, 2**31 - 1)
    rng = rng_for(seed, "global")
    recent = history.get("jobs", [])[-8:]
    ac = config["anti_repetition"]

    recent_narratives = [j.get("narrative_archetype") for j in recent[-ac["avoid_same_narrative_in_last"]:]]
    recent_visuals = [j.get("visual_grammar") for j in recent[-ac["avoid_same_visual_in_last"]:]]
    recent_music = [j.get("music_profile") for j in recent[-ac["avoid_same_music_in_last"]:]]
    recent_voices = [j.get("voice_profile") for j in recent[-ac["avoid_same_voice_in_last"]:]]
    recent_colors = [j.get("color_arc") for j in recent[-2:]]
    recent_ctas = [j.get("cta_style") for j in recent[-2:]]

    archetype = choose(config["narrative_archetypes"], rng, recent_narratives)
    primary_visual = choose(config["visual_grammars"], rng, recent_visuals)
    secondary = choose_many(config["visual_grammars"], rng, 2, [primary_visual["id"]])
    music = choose(config["music_profiles"], rng, recent_music)
    voice = choose(config["voice_direction"]["profiles"], rng, recent_voices, key="id")
    color = choose(config["color_arcs"], rng, recent_colors)
    cta_pool = [style for style in config["cta_styles"] if style not in set(recent_ctas)]
    cta_style = rng.choice(cta_pool or config["cta_styles"])

    beat_ids = archetype["beats"][:]
    if args.duracao < 45 and len(beat_ids) == 6:
        beat_ids = [beat_ids[0], beat_ids[1], beat_ids[2], beat_ids[-2], beat_ids[-1]]
    windows = make_windows(args.duracao, beat_ids)
    moves = camera_sequence(config["camera_moves"], rng, max(4, len(beat_ids)))
    transitions = [item["id"] for item in config["transitions"]]
    rng.shuffle(transitions)

    beats = []
    for i, (beat_id, start, end) in enumerate(windows):
        grammar = [primary_visual["label"], secondary[i % len(secondary)]["label"]]
        beats.append({
            "index": i + 1,
            "id": beat_id,
            "time": {"start": round(start, 2), "end": round(end, 2), "label": f"{fmt_time(start)}–{fmt_time(end)}"},
            "narrative_goal": beat_goal(beat_id, args.tema, archetype["id"]),
            "visual_grammar": grammar,
            "visual_direction": visual_direction(grammar, beat_id, args.tema),
            "camera_move": moves[i],
            "motion_notes": "Movimento contínuo, elegante e subordinado à informação; evitar zoom automático em todos os planos.",
            "transition": transitions[i % len(transitions)],
            "on_screen_text": text_direction(beat_id, args.tema, rng),
            "audio": {
                "narration": "lead",
                "music": "below_voice_with_ducking",
                "sfx": rng.choice(config["sfx_library"]),
            },
            "script_placeholder": f"{{{{TEXTO_DA_BATIDA_{i+1}}}}}",
        })

    narration_prompt = (
        f"{config['voice_direction']['base']} {voice['direction']} "
        "Write and perform only the Portuguese spoken script after the colon. "
        "Use short natural pauses after dates, numbers and revelations; do not sound rushed."
    )
    music_prompt = f"{music['direction']} Tempo target: {music['tempo_bpm'][0]}–{music['tempo_bpm'][1]} BPM. Duration: approximately {args.duracao} seconds."

    return {
        "engine": {"name": config["engine_name"], "version": config["version"]},
        "job": {
            "id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + f"-s{seed}",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "seed": seed,
            "topic": args.tema,
            "audience": args.publico,
            "objective": args.objetivo,
            "cta_text": args.cta,
            "duration_seconds": args.duracao,
            "aspect_ratio": args.formato,
            "resolution": config["defaults"]["resolution"] if args.formato == "9:16" else ("1080x1080" if args.formato == "1:1" else "1920x1080"),
        },
        "creative_direction": {
            "thesis_placeholder": f"Uma frase que explique por que {args.tema} importa.",
            "narrative_archetype": archetype["id"],
            "narrative_label": archetype["label"],
            "visual_grammar": primary_visual["id"],
            "supporting_visual_grammars": [g["id"] for g in secondary],
            "color_arc": color["id"],
            "cta_style": cta_style,
            "variation_guard": "Não repetir a mesma combinação de arquétipo, gramática visual, voz e música dos trabalhos recentes.",
        },
        "audio": {
            "voice_profile": voice["id"],
            "voice_name": voice["voice_name"],
            "narration_direction_english": narration_prompt,
            "spoken_language": "Portuguese (Brazil)",
            "language_code": "pt-BR",
            "music_profile": music["id"],
            "music_prompt_english": music_prompt,
            "mix_rules": [
                "Narration stays intelligible and in front.",
                "Duck music by approximately 8 dB under speech, then adjust by ear.",
                "Use SFX only for visible or narratively justified events.",
                "Leave a clean 1.5–2 second musical tail at the ending.",
            ],
        },
        "beats": beats,
        "production_rules": config["rendering_rules"],
        "next_inputs_needed": [
            "roteiro original ou autorização para o motor escrever o roteiro",
            "objetivo final e CTA, se diferente do padrão",
            "referências de produto, pessoa ou marca quando a fidelidade visual for necessária",
            "assets locais ou autorização para gerar imagens e vídeos complementares",
        ],
    }


def markdown_prompt_pack(plan: dict[str, Any]) -> str:
    job = plan["job"]
    creative = plan["creative_direction"]
    audio = plan["audio"]
    lines = [
        f"# Pacote de prompts — {job['topic']}",
        "",
        f"- **Formato:** {job['aspect_ratio']} / {job['resolution']} / {job['duration_seconds']} s",
        f"- **Arquétipo:** {creative['narrative_label']} (`{creative['narrative_archetype']}`)",
        f"- **Gramática visual principal:** {creative['visual_grammar']}",
        f"- **Gramáticas de apoio:** {', '.join(creative['supporting_visual_grammars'])}",
        f"- **Curva de cor:** {creative['color_arc']}",
        f"- **Estilo de CTA:** {creative['cta_style']}",
        "",
        "## Direção da narração",
        "",
        f"**Prompt de direção em inglês:** {audio['narration_direction_english']}",
        "",
        "> O texto falado deve permanecer em português brasileiro. A instrução de direção fica separada do texto falado e a narração real deve ser medida antes de travar os planos.",
        "",
        "## Direção da trilha",
        "",
        f"**Prompt de música em inglês:** {audio['music_prompt_english']}",
        "",
        "## Shot list",
        "",
    ]
    for beat in plan["beats"]:
        lines.extend([
            f"### Shot {beat['index']} — {beat['id']} ({beat['time']['label']})",
            f"- **Objetivo narrativo:** {beat['narrative_goal']}",
            f"- **Visual:** {beat['visual_direction']}",
            f"- **Movimento de câmera:** {beat['camera_move']}",
            f"- **Transição:** {beat['transition']}",
            f"- **Texto na tela:** {beat['on_screen_text']}",
            f"- **Som:** narração na frente; música abaixo; SFX: {beat['audio']['sfx']}",
            f"- **Texto falado:** `{beat['script_placeholder']}`",
            "",
        ])
    lines.extend([
        "## Checklist de montagem",
        "",
        "1. Gerar ou aprovar a narração; medir duração e, se necessário, timestamps por palavra.",
        "2. Recalcular as janelas dos shots com a duração real da narração.",
        "3. Gerar ou selecionar visuais sem repetir a mesma gramática em sequência.",
        "4. Aplicar movimentos com intenção, não como preset em todas as imagens.",
        "5. Montar trilha, ducking, efeitos, títulos e legendas.",
        "6. Verificar ritmo, legibilidade, proporção, áudio e integridade com ffprobe.",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera um plano de vídeo narrativo variado.")
    parser.add_argument("--tema", required=True, help="Assunto do vídeo")
    parser.add_argument("--duracao", type=float, default=60.0, help="Duração alvo em segundos")
    parser.add_argument("--formato", choices=["9:16", "1:1", "16:9"], default="9:16")
    parser.add_argument("--objetivo", default="educar e envolver", help="Objetivo editorial ou comercial")
    parser.add_argument("--publico", default="público geral interessado no assunto", help="Público-alvo")
    parser.add_argument("--cta", default="Saiba mais", help="Chamada para ação")
    parser.add_argument("--seed", type=int, default=None, help="Seed para repetir a mesma variação")
    parser.add_argument("--voz", default=None, help="Forçar um voice profile do config")
    parser.add_argument("--out", default=None, help="Pasta de saída; por padrão, jobs/<id>")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.duracao < 20 or args.duracao > 600:
        raise SystemExit("A duração deve ficar entre 20 e 600 segundos.")
    config = load_json(CONFIG_PATH, {})
    history = load_json(HISTORY_PATH, {"jobs": []})
    plan = build_plan(args, config, history)
    if args.voz:
        profiles = {p["id"]: p for p in config["voice_direction"]["profiles"]}
        if args.voz not in profiles:
            raise SystemExit(f"Voz desconhecida: {args.voz}. Opções: {', '.join(profiles)}")
        plan["audio"]["voice_profile"] = args.voz
        plan["audio"]["voice_name"] = profiles[args.voz]["voice_name"]
        plan["audio"]["narration_direction_english"] = f"{config['voice_direction']['base']} {profiles[args.voz]['direction']} Write and perform only the Portuguese spoken script after the colon."

    job_id = plan["job"]["id"]
    out_dir = Path(args.out).expanduser().resolve() if args.out else ROOT / "jobs" / job_id
    out_dir.mkdir(parents=True, exist_ok=True)
    save_json(out_dir / "plano.json", plan)
    (out_dir / "prompt_pack.md").write_text(markdown_prompt_pack(plan), encoding="utf-8")

    history.setdefault("jobs", []).append({
        "job_id": job_id,
        "created_at": plan["job"]["created_at"],
        "topic": args.tema,
        "seed": plan["job"]["seed"],
        "narrative_archetype": plan["creative_direction"]["narrative_archetype"],
        "visual_grammar": plan["creative_direction"]["visual_grammar"],
        "music_profile": plan["audio"]["music_profile"],
        "voice_profile": plan["audio"]["voice_profile"],
        "color_arc": plan["creative_direction"]["color_arc"],
        "cta_style": plan["creative_direction"]["cta_style"],
    })
    save_json(HISTORY_PATH, history)

    print(json.dumps({
        "job_id": job_id,
        "output_dir": str(out_dir),
        "files": [str(out_dir / "plano.json"), str(out_dir / "prompt_pack.md")],
        "selected_variation": plan["creative_direction"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
