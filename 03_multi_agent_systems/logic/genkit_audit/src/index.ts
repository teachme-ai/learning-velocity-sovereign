/**
 * src/index.ts — Sovereign Audit Committee
 * Session 03: Multi-Agent Systems with Firebase Genkit
 *
 * Flow: auditCommitteeFlow
 *   Agent 1 — Forensic Investigator  (structured output: ForensicReportSchema)
 *   Agent 2 — Risk Strategist         (structured output: StrategyDraftSchema)
 *   Agent 3 — Executive Critic        (Critic pattern: retry loop until ≥2 weaknesses)
 *
 * Run:   npm run dev
 * Trace: genkit start  →  open Developer UI → Flows → auditCommitteeFlow
 */

import { genkit, z } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';

// ── Initialise Genkit with Google AI plugin ───────────────────────────────────

const ai = genkit({
    plugins: [googleAI()],           // reads GEMINI_API_KEY from environment
});

const MODEL = googleAI.model('gemini-2.5-flash');

// ── Zod Schemas ───────────────────────────────────────────────────────────────

const ViolationSchema = z.object({
    transactionId: z.string().describe('Transaction ID'),
    rule: z.string().describe('Policy rule violated'),
    severity: z.enum(['HIGH', 'MEDIUM', 'LOW']).describe('Severity rating'),
    approvalIssue: z.string().describe('Approval chain finding'),
});

const ForensicReportSchema = z.object({
    violations: z.array(ViolationSchema).describe('List of policy violations'),
    summary: z.string().describe('Overall forensic summary'),
});

const StrategyDraftSchema = z.object({
    riskRating: z.enum(['CRITICAL', 'HIGH', 'MODERATE', 'LOW']),
    totalExposureUsd: z.number().describe('Total financial exposure in USD'),
    quarterlyBudgetImpactPct: z.number().describe('% of quarterly budget at risk'),
    mitigations: z.array(z.string()).describe('Three mitigation strategies'),
});

const CriticOutputSchema = z.object({
    weaknesses: z.array(z.string()).min(2).describe('At least two weaknesses found'),
    revisedStrategy: z.string().describe('Improved strategy addressing all weaknesses'),
});

// ── Agent System Instructions ─────────────────────────────────────────────────

const FORENSIC_SYSTEM = `You are the Forensic Investigator on the Sovereign Audit Committee.
Analyze raw expense data and identify SPECIFIC policy violations.
For each flagged transaction: state the exact rule broken, assign severity (HIGH/MEDIUM/LOW),
and assess whether the approval chain was correctly followed.
Be exhaustive and structured. Return valid JSON matching the required schema.`;

const STRATEGIST_SYSTEM = `You are the Risk Strategist on the Sovereign Audit Committee.
You receive forensic findings and assess FINANCIAL IMPACT on the quarterly budget.
Quantify total exposure, percentage of budget at risk, and assign a Risk Rating.
Propose exactly three specific mitigation strategies with projected savings.
Return valid JSON matching the required schema.`;

const CRITIC_SYSTEM = `You are the Executive Critic on the Sovereign Audit Committee.
Your role is QUALITY CONTROL — you are demanding and rigorous.
You MUST identify AT LEAST TWO specific weaknesses in the strategy presented.
Then provide a REVISED strategy that directly addresses each weakness.
Label weaknesses clearly as [WEAKNESS 1] and [WEAKNESS 2].
Do not approve without revision — that is your mandate.
Return valid JSON matching the required schema.`;

// ── Flow Input/Output ─────────────────────────────────────────────────────────

const AuditInputSchema = z.object({
    csvData: z.string().describe('Contents of flagged_expenses.csv as a plain text string'),
});

const AuditOutputSchema = z.object({
    forensicReport: ForensicReportSchema,
    strategyDraft: StrategyDraftSchema,
    criticFeedback: CriticOutputSchema,
});

// ── Main Flow ─────────────────────────────────────────────────────────────────

export const auditCommitteeFlow = ai.defineFlow(
    {
        name: 'auditCommitteeFlow',
        inputSchema: AuditInputSchema,
        outputSchema: AuditOutputSchema,
    },
    async ({ csvData }) => {

        // ── Agent 1: Forensic Investigator ──────────────────────────────────────
        console.log('\n═══ Agent 1: Forensic Investigator deliberating... ═══');
        const forensicResponse = await ai.generate({
            model: MODEL,
            system: FORENSIC_SYSTEM,
            prompt: `Analyze these flagged transactions for policy violations:\n\n${csvData}\n\nReturn your findings as structured JSON.`,
            output: { schema: ForensicReportSchema },
            config: { temperature: 0.3 },
        });
        const forensicReport = forensicResponse.output!;
        console.log('[Forensic] Violations found:', forensicReport.violations.length);
        console.log('[Forensic] Summary:', forensicReport.summary);

        // ── Agent 2: Risk Strategist ─────────────────────────────────────────────
        console.log('\n═══ Agent 2: Risk Strategist deliberating... ═══');
        const forensicText = JSON.stringify(forensicReport, null, 2);
        const strategyResponse = await ai.generate({
            model: MODEL,
            system: STRATEGIST_SYSTEM,
            prompt: `The Forensic Investigator has produced these findings:\n\n${forensicText}\n\nAssess financial impact and propose three mitigation strategies. Return structured JSON.`,
            output: { schema: StrategyDraftSchema },
            config: { temperature: 0.4 },
        });
        const strategyDraft = strategyResponse.output!;
        console.log('[Strategist] Risk Rating:', strategyDraft.riskRating);
        console.log('[Strategist] Total Exposure: $' + strategyDraft.totalExposureUsd.toLocaleString());

        // ── Agent 3: Executive Critic (with retry loop) ──────────────────────────
        console.log('\n═══ Agent 3: Executive Critic reviewing... ═══');
        const strategyText = JSON.stringify(strategyDraft, null, 2);
        let criticFeedback: z.infer<typeof CriticOutputSchema> | null = null;
        const MAX_RETRIES = 3;

        for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
            console.log(`[Critic] Review attempt ${attempt}/${MAX_RETRIES}...`);
            const criticResponse = await ai.generate({
                model: MODEL,
                system: CRITIC_SYSTEM,
                prompt: `The Risk Strategist has produced this analysis:\n\n${strategyText}\n\nCritique this strategy. Find AT LEAST TWO weaknesses, then produce a revised version. Return structured JSON.`,
                output: { schema: CriticOutputSchema },
                config: { temperature: 0.6 },
            });

            const candidate = criticResponse.output!;

            if (candidate.weaknesses.length >= 2) {
                criticFeedback = candidate;
                console.log(`[Critic] ✅ Found ${candidate.weaknesses.length} weaknesses. Quality gate passed.`);
                candidate.weaknesses.forEach((w, i) => console.log(`  [WEAKNESS ${i + 1}] ${w}`));
                break;
            }

            console.log(`[Critic] ⚠️  Only ${candidate.weaknesses.length} weakness found — retrying...`);
        }

        if (!criticFeedback) {
            throw new Error('Executive Critic failed to produce ≥2 weaknesses after max retries.');
        }

        // ── Return full committee report ─────────────────────────────────────────
        console.log('\n═══ Committee deliberation complete. ═══');
        return { forensicReport, strategyDraft, criticFeedback };
    }
);
