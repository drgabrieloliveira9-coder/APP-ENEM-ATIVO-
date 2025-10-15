export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "13.0.5"
  }
  public: {
    Tables: {
      essays: {
        Row: {
          content: string
          created_at: string | null
          feedback: string | null
          id: string
          score: number | null
          title: string
          user_id: string | null
        }
        Insert: {
          content: string
          created_at?: string | null
          feedback?: string | null
          id?: string
          score?: number | null
          title: string
          user_id?: string | null
        }
        Update: {
          content?: string
          created_at?: string | null
          feedback?: string | null
          id?: string
          score?: number | null
          title?: string
          user_id?: string | null
        }
        Relationships: []
      }
      question_attempts: {
        Row: {
          created_at: string | null
          id: string
          is_correct: boolean
          question_id: string | null
          user_answer: string
          user_id: string | null
        }
        Insert: {
          created_at?: string | null
          id?: string
          is_correct: boolean
          question_id?: string | null
          user_answer: string
          user_id?: string | null
        }
        Update: {
          created_at?: string | null
          id?: string
          is_correct?: boolean
          question_id?: string | null
          user_answer?: string
          user_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "question_attempts_question_id_fkey"
            columns: ["question_id"]
            isOneToOne: false
            referencedRelation: "questions"
            referencedColumns: ["id"]
          },
        ]
      }
      questions: {
        Row: {
          area: Database["public"]["Enums"]["question_area"]
          correct_answer: string
          created_at: string | null
          explanation: string
          id: string
          option_a: string
          option_b: string
          option_c: string
          option_d: string
          option_e: string
          question: string
          subject: string
        }
        Insert: {
          area: Database["public"]["Enums"]["question_area"]
          correct_answer: string
          created_at?: string | null
          explanation: string
          id?: string
          option_a: string
          option_b: string
          option_c: string
          option_d: string
          option_e: string
          question: string
          subject: string
        }
        Update: {
          area?: Database["public"]["Enums"]["question_area"]
          correct_answer?: string
          created_at?: string | null
          explanation?: string
          id?: string
          option_a?: string
          option_b?: string
          option_c?: string
          option_d?: string
          option_e?: string
          question?: string
          subject?: string
        }
        Relationships: []
      }
      schedules: {
        Row: {
          created_at: string | null
          days_until_exam: number
          hours_per_day: number
          id: string
          schedule_data: Json
          user_id: string | null
        }
        Insert: {
          created_at?: string | null
          days_until_exam: number
          hours_per_day: number
          id?: string
          schedule_data: Json
          user_id?: string | null
        }
        Update: {
          created_at?: string | null
          days_until_exam?: number
          hours_per_day?: number
          id?: string
          schedule_data?: Json
          user_id?: string | null
        }
        Relationships: []
      }
      user_progress: {
        Row: {
          essays_written: number | null
          id: string
          questions_answered: number | null
          questions_correct: number | null
          study_days_completed: number | null
          total_score: number | null
          updated_at: string | null
          user_id: string | null
        }
        Insert: {
          essays_written?: number | null
          id?: string
          questions_answered?: number | null
          questions_correct?: number | null
          study_days_completed?: number | null
          total_score?: number | null
          updated_at?: string | null
          user_id?: string | null
        }
        Update: {
          essays_written?: number | null
          id?: string
          questions_answered?: number | null
          questions_correct?: number | null
          study_days_completed?: number | null
          total_score?: number | null
          updated_at?: string | null
          user_id?: string | null
        }
        Relationships: []
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      question_area:
        | "Linguagens"
        | "Matemática"
        | "Ciências Humanas"
        | "Ciências da Natureza"
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {
      question_area: [
        "Linguagens",
        "Matemática",
        "Ciências Humanas",
        "Ciências da Natureza",
      ],
    },
  },
} as const
