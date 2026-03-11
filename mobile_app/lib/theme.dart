import 'package:flutter/material.dart';

// ═══ APP COLORS (matching web CSS variables) ═══
class AppColors {
  static const Color primary = Color(0xFF8B4513); // --primary-color
  static const Color primaryLight = Color(0xFFA0522D);
  static const Color accent = Color(0xFFD4A862);
  static const Color background = Color(0xFFF8F5F0);
  static const Color cardBg = Colors.white;
  static const Color textMain = Color(0xFF2D2D2D);
  static const Color textMuted = Color(0xFF8C8C8C);
  static const Color success = Color(0xFF388E3C);
  static const Color warning = Color(0xFFF57C00);
  static const Color danger = Color(0xFFD32F2F);
  static const Color info = Color(0xFF0288D1);
  static const Color gold = Color(0xFFFCA311);
}

// ═══ APP TEXT STYLES ═══
class AppTextStyles {
  static const TextStyle heading = TextStyle(
    fontFamily: 'Georgia',
    fontWeight: FontWeight.bold,
    color: AppColors.textMain,
  );

  static const TextStyle body = TextStyle(
    fontSize: 14,
    color: AppColors.textMain,
  );

  static const TextStyle muted = TextStyle(
    fontSize: 13,
    color: AppColors.textMuted,
  );

  static const TextStyle label = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.w600,
    color: AppColors.textMuted,
    letterSpacing: 1.5,
  );
}

// ═══ APP THEME ═══
ThemeData appTheme() {
  return ThemeData(
    fontFamily: 'Inter',
    scaffoldBackgroundColor: AppColors.background,
    primaryColor: AppColors.primary,
    colorScheme: ColorScheme.fromSeed(
      seedColor: AppColors.primary,
      primary: AppColors.primary,
      secondary: AppColors.accent,
      surface: AppColors.cardBg,
      background: AppColors.background,
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: Colors.white,
      elevation: 0.5,
      centerTitle: true,
      iconTheme: IconThemeData(color: AppColors.primary),
      titleTextStyle: TextStyle(
        fontFamily: 'Georgia',
        fontWeight: FontWeight.bold,
        fontSize: 18,
        color: AppColors.textMain,
      ),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
        textStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: Colors.white,
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: AppColors.primary.withOpacity(0.15)),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: AppColors.primary.withOpacity(0.15)),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.primary, width: 1.5),
      ),
      hintStyle: TextStyle(color: AppColors.textMuted.withOpacity(0.6)),
    ),
    cardTheme: CardThemeData(
      color: Colors.white,
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      margin: const EdgeInsets.only(bottom: 12),
    ),
  );
}
