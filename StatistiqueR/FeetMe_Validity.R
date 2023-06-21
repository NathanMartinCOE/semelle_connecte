library(flextable)
library(rstatix)
library(ggplot2)
library(ggpubr)
library(plyr)

DataPath = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\MSE\\DatFrame_all_metric.csv"
DataFrame <- read.csv(DataPath)

### ====================== Instantiates vectors with a "delete" value to check that it hasn't been taken ============================

# Vectors for tab Results
normal_ground    = "delete"
mottek_vL12_vR12 = "delete"
mottek_vL12_vR14 = "delete"
mottek_vL12_vR16 = "delete"
mottek_vL12_vR18 = "delete"
mottek_vL14_vR12 = "delete"
mottek_vL16_vR12 = "delete"
mottek_vL18_vR12 = "delete"

# Digits for round in tab Results
dig_mean = 1
dig_std  = 1
dig_diff = 1
dig_p    = 3


### ====================== Iteration for compute boxplot and t_test for each parametre  =============================================

metrics = c("stanceDuration (ms)", "singleSupportDuration (ms)", "doubleSupportDuration (ms)", "swingDuration (ms)")

for (metric in metrics){
  df <- subset(DataFrame, Metric == metric)
  df$Mean = rowMeans(df[, 7:368], na.rm = TRUE)
  
  Std = -1000
  for (col in seq(1,54)){
    Std <- c(Std, sd(df[col, 7:368], na.rm = TRUE))
  }
  df$Std = Std[2:55]
  
  
  condition_order <- unique(df$Condition)
  df$Condition <- factor(df$Condition, levels = condition_order)
  
  stat.test  <- df %>%
                group_by(Condition) %>%
                t_test(Mean ~ Leg,paired=FALSE) %>%
                adjust_pvalue(method = "bonferroni") %>%
                add_significance("p.adj")
  print(stat.test)
  
  stat.test <- stat.test %>%
                add_xy_position(x = "Condition", dodge = 0.8)
  
  metric_plot <- ggboxplot(
                 df, x = "Condition", y = "Mean", 
                 color = "Leg", palette = c("#FF0000", "#0000FF"),
                 ylab=metric,xlab="Condition",xaxt="n"
                 )
  
  metric_plot <- metric_plot + stat_pvalue_manual(stat.test,label = "{p.adj.signif}", tip.length = 0)
  print(metric_plot)
  
  ggsave(paste0("C:\\Users\\Nathan\\Desktop\\Recherche\\R_studio\\FeetMe_Validity\\",metric,"_by_Leg.png"), width = 15, height = 8, device='png', dpi=700)
  
  normal_ground = c(normal_ground, 
                    paste(round(mean(df$Mean[df$Condition == "normal_ground" & df$Leg == "LeftLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "normal_ground" & df$Leg == "LeftLeg"]), digits = dig_std), sep = " "),
                    paste(round(mean(df$Mean[df$Condition == "normal_ground" & df$Leg == "RightLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "normal_ground" & df$Leg == "RightLeg"]), digits = dig_std), sep = " "),
                    paste(round(stat.test$df[stat.test$Condition == "normal_ground"], digits = dig_diff), " (",
                          round(stat.test$p.adj[stat.test$Condition == "normal_ground"], digits = dig_p), ")", sep=""))
  mottek_vL12_vR12 = c(mottek_vL12_vR12, 
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL12_vR12" & df$Leg == "LeftLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL12_vR12" & df$Leg == "LeftLeg"]), digits = dig_std), sep = " "),
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL12_vR12" & df$Leg == "RightLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL12_vR12" & df$Leg == "RightLeg"]), digits = dig_std), sep = " "),
                    paste(round(stat.test$df[stat.test$Condition == "mottek_vL12_vR12"], digits = dig_diff), " (",
                          round(stat.test$p.adj[stat.test$Condition == "mottek_vL12_vR12"], digits = dig_p), ")", sep=""))
  mottek_vL12_vR14 = c(mottek_vL12_vR14, 
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL12_vR14" & df$Leg == "LeftLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL12_vR14" & df$Leg == "LeftLeg"]), digits = dig_std), sep = " "),
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL12_vR14" & df$Leg == "RightLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL12_vR14" & df$Leg == "RightLeg"]), digits = dig_std), sep = " "),
                    paste(round(stat.test$df[stat.test$Condition == "mottek_vL12_vR14"], digits = dig_diff), " (",
                          round(stat.test$p.adj[stat.test$Condition == "mottek_vL12_vR14"], digits = dig_p), ")", sep=""))
  mottek_vL12_vR16 = c(mottek_vL12_vR16, 
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL12_vR16" & df$Leg == "LeftLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL12_vR16" & df$Leg == "LeftLeg"]), digits = dig_std), sep = " "),
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL12_vR16" & df$Leg == "RightLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL12_vR16" & df$Leg == "RightLeg"]), digits = dig_std), sep = " "),
                    paste(round(stat.test$df[stat.test$Condition == "mottek_vL12_vR16"], digits = dig_diff), " (",
                          round(stat.test$p.adj[stat.test$Condition == "mottek_vL12_vR16"], digits = dig_p), ")", sep=""))
  mottek_vL12_vR18 = c(mottek_vL12_vR18, 
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL12_vR18" & df$Leg == "LeftLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL12_vR18" & df$Leg == "LeftLeg"]), digits = dig_std), sep = " "),
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL12_vR18" & df$Leg == "RightLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL12_vR18" & df$Leg == "RightLeg"]), digits = dig_std), sep = " "),
                    paste(round(stat.test$df[stat.test$Condition == "mottek_vL12_vR18"], digits = dig_diff), " (",
                          round(stat.test$p.adj[stat.test$Condition == "mottek_vL12_vR18"], digits = dig_p), ")", sep=""))
  mottek_vL14_vR12 = c(mottek_vL14_vR12, 
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL14_vR12" & df$Leg == "LeftLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL14_vR12" & df$Leg == "LeftLeg"]), digits = dig_std), sep = " "),
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL14_vR12" & df$Leg == "RightLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL14_vR12" & df$Leg == "RightLeg"]), digits = dig_std), sep = " "),
                    paste(round(stat.test$df[stat.test$Condition == "mottek_vL14_vR12"], digits = dig_diff), " (",
                          round(stat.test$p.adj[stat.test$Condition == "mottek_vL14_vR12"], digits = dig_p), ")", sep=""))
  mottek_vL16_vR12 = c(mottek_vL16_vR12, 
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL16_vR12" & df$Leg == "LeftLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL16_vR12" & df$Leg == "LeftLeg"]), digits = dig_std), sep = " "),
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL16_vR12" & df$Leg == "RightLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL16_vR12" & df$Leg == "RightLeg"]), digits = dig_std), sep = " "),
                    paste(round(stat.test$df[stat.test$Condition == "mottek_vL16_vR12"], digits = dig_diff), " (",
                          round(stat.test$p.adj[stat.test$Condition == "mottek_vL16_vR12"], digits = dig_p), ")", sep=""))
  mottek_vL18_vR12 = c(mottek_vL18_vR12, 
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL18_vR12" & df$Leg == "LeftLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL18_vR12" & df$Leg == "LeftLeg"]), digits = dig_std), sep = " "),
                    paste(round(mean(df$Mean[df$Condition == "mottek_vL18_vR12" & df$Leg == "RightLeg"]), digits = dig_mean), "±",
                          round(mean(df$Std[df$Condition == "mottek_vL18_vR12" & df$Leg == "RightLeg"]), digits = dig_std), sep = " "),
                    paste(round(stat.test$df[stat.test$Condition == "mottek_vL18_vR12"], digits = dig_diff), " (",
                          round(stat.test$p.adj[stat.test$Condition == "mottek_vL18_vR12"], digits = dig_p), ")", sep=""))
}


### ==================================================== Creation of Results Table ======================================
names_parametre <- c(rep("Stance Duration",3),
                     rep("Single Support Duration",3), 
                     rep("Double Support Duration",3),
                     rep("Swing Duration",3))

Results <- data.frame(
  "Paramètres"       = names_parametre,
  "Leg"              = c(rep(c("Left", "Right","p-value"),4)),
  "normal_ground"    = normal_ground[2:13],
  "mottek_vL12_vR12" = mottek_vL12_vR12[2:13],
  "mottek_vL12_vR14" = mottek_vL12_vR14[2:13],
  "mottek_vL12_vR16" = mottek_vL12_vR16[2:13],
  "mottek_vL12_vR18" = mottek_vL12_vR18[2:13],
  "mottek_vL14_vR12" = mottek_vL14_vR12[2:13],
  "mottek_vL16_vR12" = mottek_vL16_vR12[2:13],
  "mottek_vL18_vR12" = mottek_vL18_vR12[2:13])

ft <- flextable(Results)
ft <- theme_vanilla(ft)
ft <- width(ft, j = 1:10, width = dim_pretty(ft)$widths)
ft <- align(ft, align = "center", part = "header")
ft <- align(ft, i = 1:12, j = 1:10, align = "center")
ft <- bg(ft,i = c(1,3,5,7,9,11), bg = "lightgrey")
ft

save_as_docx(ft, path="C:\\Users\\Nathan\\Desktop\\Recherche\\R_studio\\FeetMe_Validity\\Results_table.docx")



### ================================================ interupt ===========================================================



# This code plot the comparaison beetween conditions for each leg

metrics = c("stanceDuration (ms)", "singleSupportDuration (ms)", "doubleSupportDuration (ms)", "swingDuration (ms)")

for (metric in metrics){

  df <- subset(DataFrame, Metric == metric)
  df$Mean = rowMeans(df[, 7:368], na.rm = TRUE)
  
  condition_order <- unique(df$Condition)
  df$Condition <- factor(df$Condition, levels = condition_order)
  
  stat.test  <- df %>%
    group_by(Leg) %>%
    t_test(Mean ~ Condition,paired=FALSE) %>%
    adjust_pvalue(method = "bonferroni") %>%
    add_significance("p.adj")
  print(stat.test)
  
  stat.test <- stat.test %>%
    add_xy_position(x = "Leg", dodge = 0.8)
  
  significant_stats <- stat.test %>%
    filter(p.adj < 0.05)
  
  metric_plot <- ggboxplot(
    df, x = "Leg", y = "Mean", 
    color = "Condition",
    ylab = metric, xlab = "Leg", xaxt = "n"
  )
  
  metric_plot <- metric_plot + 
    stat_pvalue_manual(significant_stats, label = "{p.adj.signif}", tip.length = 0)
  
  print(metric_plot)
  
  ggsave(paste0("C:\\Users\\Nathan\\Desktop\\Recherche\\R_studio\\FeetMe_Validity\\",metric,"_by_Condition.png"), width = 15, height = 8, device='png', dpi=700)
  
  ft2 <- flextable(stat.test[c(1,3,4,8,10,11)])
  
  save_as_docx(ft2, path=paste0("C:\\Users\\Nathan\\Desktop\\Recherche\\R_studio\\FeetMe_Validity\\",metric,"_by_condition_pvalue.docx"))
}





### for Procédure expérimentale 

df <- subset(DataFrame, Metric == "stanceDuration (ms)")
n_step_L = 0
n_step_R = 0

for (step in seq(3:27)){
  n_step_L = n_step_L + length(df_L[step, 7:368][!is.na(df_L[step, 7:368])])
  n_step_R = n_step_R + length(df_R[step, 7:368][!is.na(df_R[step, 7:368])])
}


df <- subset(DataFrame, Metric == "stanceDuration (ms)" & Condition == "normal_ground")
df <- subset(DataFrame, Metric == "stanceDuration (ms)" & Condition == "mottek_vL18_vR12")

df_L = subset(df, Leg == "LeftLeg")
df_R = subset(df, Leg == "RightLeg")

step_L = -100
step_R = -100

for (step in seq(3:length(df_L$Step_0))){
  step_L = c(step_L , length(df_L[step, 7:368][!is.na(df_L[step, 7:368])]))
  step_R = c(step_R , length(df_R[step, 7:368][!is.na(df_R[step, 7:368])]))
}

step_L = step_L[2:length(df_L$Step_0)]
step_R = step_R[2:length(df_L$Step_0)]

mean(step_L, na.rm = TRUE)
sd(step_L,  na.rm = TRUE)
mean(step_R, na.rm = TRUE)
sd(step_R,  na.rm = TRUE)

# stop









# save a function to do ANOVA
ANOVA_factory <- function(){
  ### =========================================== Anova à 2 facteurs ==================================
  
  library(emmeans)
  
  ### ========================================== Vérifier les hypothèses ==============================
  # Construire le modèle linéaire
  model  <- lm(Mean ~ Leg*Condition,
               data = df)
  # Créer un QQ plot des résidus
  ggqqplot(residuals(model))
  
  # Calculer le test de normalité de Shapiro-Wilk --> Le score est normalement distribué si (p > 0,05)
  shapiro_test(residuals(model))
  
  # Test d'hypothèse de normalité par groupe
  df %>%
    group_by(Leg, Condition) %>%
    shapiro_test(Mean)
  
  # Créer des graphiques QQ plots pour chaque
  ggqqplot(df, "Mean", ggtheme = theme_bw()) +
    facet_grid(Leg ~ Condition)
  
  # Hypothèse d'homogénéité des variances --> Les variances sont homogènes dans les différents groupes si (p > 0,05) 
  df %>% levene_test(Mean ~ Leg*Condition)
  
  ### ======================================= Calculs ===================================================
  
  # Calcul ANOVA
  res.aov <- df %>% anova_test(Mean ~ Leg * Condition)
  res.aov
  
  # Calculer des effets principaux
  model <- lm(Mean ~ Leg * Condition, data = df)
  df %>%
    group_by(Condition) %>%
    anova_test(Mean ~ Leg, error = model)
  
  # Calculer des comparaisons par paires
  pwc <- df %>% 
    group_by(Condition) %>%
    emmeans_test(Mean ~ Leg, p.adjust.method = "bonferroni") 
  pwc
}


### ============================================== Repetability ===========================================

conditions = c("normal_ground", "mottek_vL12_vR12", "mottek_vL14_vR12", "mottek_vL16_vR12", "mottek_vL18_vR12", "mottek_vL12_vR14", "mottek_vL12_vR16", "mottek_vL12_vR18")

for (metric in metrics){
  for (condition in conditions){
    df <- subset(DataFrame, Metric == metric & Condition == condition)
    df$Mean = rowMeans(df[, 7:368], na.rm = TRUE)
    
    stat.test  <- df %>%
      t_test(Mean ~ N_test,paired=FALSE) %>%
      adjust_pvalue(method = "bonferroni") %>%
      add_significance("p.adj")
    print(paste("Metric:", metric, "Condition:", condition, sep = " "))
    print(stat.test)
    
    stat.test <- stat.test %>%
      add_xy_position(x = "Condition", dodge = 0.8)
    
    metric_plot <- ggboxplot(
      df, x = "N_test", y = "Mean", 
      ylab=metric,xlab="N_test",xaxt="n"
    )
    
    metric_plot <- metric_plot + stat_pvalue_manual(stat.test,label = "{p.adj.signif}", tip.length = 0)
    print(metric_plot)
    
  } # end for condition
}   # end for metric




