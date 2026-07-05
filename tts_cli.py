import argparse
import asyncio
import edge_tts

async def amain(text, output, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-v", "--voice", default="zh-CN-XiaoyiNeural")
    args = parser.parse_args()
    
    print(f"[TTS] Generating: {args.text}")
    asyncio.run(amain(args.text, args.output, args.voice))
    print(f"[TTS] Saved to: {args.output}")