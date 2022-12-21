library(ggplot2)
library(ggpmisc)
library(gridExtra)
library(showtext)

font_add_google("Source Sans Pro", regular.wt = 300)
font_add_google("JetBrains Mono")
font_add_google("Source Serif Pro")

showtext_auto()

results <- read.csv("results/complete_12-14.csv")

results <- results[-c(1:2, 4:10)]

plot_data_column_name <- function(data, column, name) {
        p <- ggplot(data, aes(x = year, y = data[, column])) +
                # ggtitle("Num Sents") +
                xlab("year") +
                ylab(name) +
                geom_point(color = "#737373", size = 0.1) +
                geom_smooth(
                        method = lm, color = "#b31414",
                        fill = "#ffbfbf", fullrange = TRUE, linewidth = 0.5
                ) +
                theme(
                        panel.background = element_rect(fill = "#f4f4f4"),
                        panel.grid.major.y = element_line(
                                linetype = "dotted", color = "#bdbdbd"
                        ),
                        panel.grid.major.x = element_blank(),
                        panel.grid.minor = element_blank(),
                        text = element_text(
                                family = "Source Sans Pro",
                                size = 36
                        ),
                        plot.title = element_text(
                                family = "Source Sans Pro",
                                face = "bold", size = 54,
                                margin = margin(b = 10)
                        ),
                        axis.text = element_text(color = "#9c9c9c"),
                        axis.title = element_text(
                                family = "JetBrains Mono",
                                color = "#4f4f4f"
                        ),
                        axis.title.y = element_text(margin = margin(r = 5)),
                        axis.title.x = element_text(margin = margin(t = 5)),
                        axis.text.y = element_text(margin = margin(r = 5)),
                        axis.text.x = element_text(margin = margin(t = 5)),
                        axis.ticks.y = element_blank(),
                        axis.ticks.x = element_line(color = "#9e9e9e"),
                        axis.ticks.length = unit(5, "pt"),
                        axis.line.x = element_line(color = "#9e9e9e"),
                        plot.margin = margin(t = 5, b = 2, r = 2, l = 2),
                )
}

plot_data_column <- function(data, column) {
        plot_data_column_name(data, column, column)
}

small_plot <- function(data, column) {
        plot_data_column(data, column) +
                theme(
                        text = element_text(size = 10),
                        plot.margin = margin(t = 15, b = 15, r = 10, l = 10)
                ) +
                stat_poly_eq(aes(family = "Source Sans Pro"))
}


myplots <- lapply(colnames(results[-1]), small_plot, data = results)

# do.call("grid.arrange", c(myplots[1:10], ncol = 4))

# g <- arrangeGrob(grobs = myplots, ncol = 4)
# ggsave("grobs.png", g, width = 8.5, height = 16, type = "cairo", dpi = 300)


plot_file_name <- function(file, name) {
        p <- plot_data_column_name(results, file, name)
        ggsave(paste("analysis/export/", file, ".png", sep = ""), p,
                width = 4.25, height = 3, type = "cairo",
                dpi = 300
        )
}

plot_file <- function(file) {
        plot_file_name(file, file)
}

tags <- c(
        "avg_stopless_aoa_min",
        "stop_words_per_sentence",
        "avg_sentence_length_by_word",
        "avg_tree_edit_dist_adjacent",
        "avg_clause_length",
        "avg_aoa_min",
        "avg_dependency_distance",
        "avg_word_freq_stopless",
        "avg_node_depth",
        "avg_words_before_root",
        "clauses_per_sent",
        "avg_max_clause_depth",
        "avg_node_clause_depth",
        "max_dependency_distance",
        "max_node_clause_depth",
        "loose_parataxis_per_sent",
        "root_parataxis_per_sent_loose",
        "root_parataxis_per_sent_strict",
        "avg_word_freq_uniq"
)

# for (f in tags) {
#         plot_file(f)
# }

# plot_file_name("root_parataxis_per_sent_strict", "root_parataxis_strict")
# plot_file_name("root_parataxis_per_sent_loose", "root_parataxis_loose")
# plot_file_name("avg_tree_edit_dist_adjacent", "avg_tree_edit_dist_adj")
# plot_file_name("avg_sentence_length_by_word", "avg_sentence_len_by_word")
plot_file("avg_np_length")