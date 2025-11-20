# CONOPS — RF Battlespace Awareness Simulator

## Mission
Provide real-time, passive geolocation of adversary RF emitters using a proliferated LEO satellite constellation — from tactical edge to strategic level.

## Target Set
- Enemy C2 nodes, air-defense radars, jammers, SATCOM terminals, drone control links, HF/VHF/UHF/SHF emitters operating 100 kHz – 40 GHz.

## Concept
1. **Detection**  
   8–32 LEO smallsats with wideband SDR payloads continuously scan the battlespace.

2. **Measurement**  
   Each satellite records time-of-arrival (TOA) and frequency-of-arrival (FOA) of detected pulses.

3. **Geolocation**  
   Onboard edge processing or ground segment fuses TDOA + FDOA measurements → instantaneous single-satellite-pair fix.

4. **Tracking**  
   Extended Kalman Filter (EKF) maintains continuous track through emitter maneuvers and constellation handovers.

5. **Dissemination**  
   Tracks pushed in real time to JTAC, JADC2, fires network, or autonomous kill chains.

## Performance (current demo)
| Metric              | Value         | Notes                              |
|---------------------|---------------|------------------------------------|
| Constellation       | 8 × 550 km LEO, 53° incl.            | Walker-like spacing                |
| Fix latency         | < 2 seconds                          | From detection to display          |
| CEP95 (good geometry) | 30–150 m                            | 10 ns TOA + 5 Hz FDOA noise        |
| CEP95 (poor geometry) | 1–15 km                             | Visualized as red/yellow ellipse   |
| Update rate         | 0.2 Hz (every 5 s)                   | Demo limited — real system > 1 Hz  |

## Kill Chain Integration
Emitter → Detection → TDOA/FDOA Fix → Kalman Track → Task via JADC2 → Weapon Release
<─────────────── 8 seconds median ───────────────>

## Roadmap
- [x] Static emitter TDOA (current)
- [ ] Moving drone swarm + FDOA
- [ ] EKF track smoothing + track continuity
- [ ] Multi-constellation fusion (LEO + MEO + GEO)
- [ ] Real TLEs + orbital propagation
- [ ] Export to STANAG 4607 / Cursor-on-Target

Apache 2.0 — built in public — no classified data or ITAR