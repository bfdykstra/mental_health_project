export interface TherapyRequest {
  user_query: string
  keywords?: string[]
  top_k: number
}

export interface SimilarExample {
  prompt: string
  similarity_score?: number
  metadata?: Record<string, any>
}

export interface TherapyResponse {
  similar_examples: SimilarExample[]
  synthesized_response: string
  keywords: string[]
  user_query: string
}

export const THERAPY_KEYWORDS = [
  "Anxiety",
  "Behavioral Challenges",
  "Body Image & Eating Disorders",
  "Chronic Illness & Mental Health",
  "Communication & Conflict Resolution",
  "Coping Strategies",
  "Decision-Making & Motivation",
  "Depression",
  "Family Dynamics",
  "Grief & Loss",
  "Healthcare Trust & Access",
  "Identity",
  "Life Transitions & Adjustment",
  "Medication & Treatment Adherence",
  "Mood Disorders",
  "Nutrition & Food Habits",
  "Other",
  "Parenting & Child Behavior",
  "Physical Activity & Lifestyle",
  "Romantic & Intimate Relationships",
  "Self-Esteem & Identity",
  "Sleep & Fatigue",
  "Social Connection & Isolation",
  "Stigma & Social Norms",
  "Stress & Burnout",
  "Substance Use & Addiction",
  "Support Systems & Caregiving",
  "Therapeutic Engagement",
  "Trauma & PTSD",
  "Trust & Safety",
  "Weight Management",
  "Youth & Adolescence",
] as const
