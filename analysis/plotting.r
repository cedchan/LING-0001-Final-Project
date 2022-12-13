library(ggplot2)
library(gridExtra)
library(showtext)

font_add_google("Source Sans Pro", regular.wt = 300)
font_add_google("JetBrains Mono")
font_add_google("Source Serif Pro")

showtext_auto()

results <- read.csv("results/complete_12-10.csv")

results <- results[-c(1:2, 4:10)]

plot_data_column = function (data, column) {
        p <- ggplot(data, aes(x=year, y=data[, column])) +
                ggtitle("Num Sents") +
                xlab("year") +
                ylab(column) +           
                geom_point(color="#737373", size=0.1) +
                geom_smooth(method=lm, color="#b31414", fill="#ffbfbf", fullrange=TRUE, linewidth=0.5) +
                # scale_x_continuous(expand = c(0, 0), limits = range(data$year)) + 
                theme(
                        panel.background = element_rect(fill = "#f4f4f4"),
                        panel.grid.major.y = element_line(linetype="dotted", color="#bdbdbd"),
                        panel.grid.major.x = element_blank(), 
                        panel.grid.minor = element_blank(),

                        text=element_text(family="Source Sans Pro", size=36),
                        plot.title=element_text(family="Source Sans Pro", face="bold", size=54, margin=margin(b=10)),
                        
                        axis.text=element_text(color="#9c9c9c"),
                        axis.title=element_text(family = "JetBrains Mono", color="#4f4f4f"),
                        axis.title.y=element_text(margin=margin(r=5)),
                        axis.title.x=element_text(margin=margin(t=5)),
                        axis.text.y=element_text(margin=margin(r=5)),
                        axis.text.x=element_text(margin=margin(t=5)),
                        axis.ticks.y = element_blank(),
                        axis.ticks.x = element_line(color = "#9e9e9e"),
                        axis.ticks.length = unit(5,"pt"),
                        axis.line.x = element_line(color="#9e9e9e"),
                        
                        plot.margin=margin(t=0, b=0, r=0, l=0),
                ) 
        # if (min(data[, column]) < 10) {
        #         p <- p + scale_y_continuous(expand = c(0, 0), limits = c(0, NA))
        # }
        p
}

myplots <- lapply(colnames(results[-1]), plot_data_column, data = results)

# do.call("grid.arrange", myplots[1:2])

# do.call("ggsave", myplots[1:1], "test%03d.png")

p1 <- plot_data_column(results, "num_tokens")
p2 <- plot_data_column(results, "num_tokens")
p3 <- plot_data_column(results, "num_tokens")
p4 <- plot_data_column(results, "num_tokens")

# png("Test.png", width=8.5, height=9, type = "cairo", unit="in", res=300)
# grid.arrange(p1, p2, p3, p4, p3, p3, ncol=2)
# dev.off()

ggsave("small.png", p1, width=4.25, height=3, type="cairo", dpi=300)

# ggsave("hf.png", plot_data_column(results, "num_tokens"), width=8.5, height=6, type = "cairo", dpi=300)
# print(plot_data_column(results, "num_tokens"))
# print(myplots[1])

# myplots[1] + 
