import { type NextRequest, NextResponse } from "next/server"
import type { TherapyRequest, TherapyResponse } from "@/types/therapy"

export async function POST(request: NextRequest) {
  try {
    const body: TherapyRequest = await request.json()

    // Simulate API processing delay
    await new Promise((resolve) => setTimeout(resolve, 1500))

    // Mock response data
    const mockResponse: TherapyResponse = {
      similar_examples: [
        {
          prompt: "Patient expressing work-life balance struggles and burnout symptoms",
          similarity_score: 0.92,
          metadata: { source: "therapy_examples_db", category: "stress_management" },
        },
        {
          prompt: "Client discussing overwhelming responsibilities and desire to escape",
          similarity_score: 0.87,
          metadata: { source: "therapy_examples_db", category: "coping_strategies" },
        },
        {
          prompt: "Individual reporting chronic stress and lack of personal time",
          similarity_score: 0.84,
          metadata: { source: "therapy_examples_db", category: "self_care" },
        },
        {
          prompt: "Patient describing feelings of being trapped by obligations",
          similarity_score: 0.81,
          metadata: { source: "therapy_examples_db", category: "boundary_setting" },
        },
        {
          prompt: "Client expressing burnout and need for stress management techniques",
          similarity_score: 0.78,
          metadata: { source: "therapy_examples_db", category: "stress_reduction" },
        },
      ],
      synthesized_response: `Based on the patient's expression of feeling overwhelmed with work and family responsibilities, along with burnout symptoms and thoughts of escape, here are some therapeutic approaches to consider:

**Immediate Response:**
- Validate their feelings: "It sounds like you're carrying a heavy load right now, and feeling overwhelmed is a natural response to that."
- Normalize the experience: "Many people struggle with balancing multiple responsibilities, and burnout is more common than you might think."

**Therapeutic Interventions:**
1. **Stress Assessment**: Help them identify specific stressors and their impact
2. **Boundary Setting**: Explore what boundaries they can establish between work and personal life
3. **Self-Care Planning**: Develop realistic self-care strategies that fit their schedule
4. **Cognitive Restructuring**: Address any guilt or perfectionist thinking patterns
5. **Support System Evaluation**: Identify available support and how to access it

**Questions to Explore:**
- "What would 'finding time for yourself' look like in practical terms?"
- "When you think about running away, what are you hoping to escape from specifically?"
- "What small changes could you make this week to create some breathing room?"

**Safety Considerations:**
Monitor for signs of depression or more serious mental health concerns if the desire to "run away" intensifies or becomes more specific.`,
      keywords: body.keywords || [],
      user_query: body.user_query,
    }

    return NextResponse.json(mockResponse)
  } catch (error) {
    console.error("Error processing therapy request:", error)
    return NextResponse.json({ error: "Failed to process request" }, { status: 500 })
  }
}
