library(ggplot2)
library(gridExtra)
results <- read.csv("results/complete_12-10.csv")

# setkey(data, V1)
# setindex(data, V1)

# print(range(x["num_words", 2:62]))
# print(length(x["num_words"]))

# x1 <- data["num_sentences", -1]
# y1 <- data["num_words", -1]

# tx <- as.vector(as.matrix(x1))
# ty <- as.vector(as.matrix(y1))

# graphs <- list()
# for (col in colnames(data[-(1:10)])) {
#     p <- ggplot(data, aes(x=year, y=col)) +
#         geom_point() +
#         geom_smooth(method=lm , color="red", fill="#69b3a2", se=TRUE)
#     print(p)
#     graphs <- append(graphs, p)
# }
results <- results[-(4:10)]
results <- results[-(1:2)]

plot_data_column = function (data, column) {
    ggplot(data, aes(x=year, y=data[,column])) +
        ylab(column) +             
        geom_point() +
        geom_smooth(method=lm , color="red", fill="#69b3a2", se=TRUE)
}

myplots <- lapply(colnames(results[-1]), plot_data_column, data = results)

# # print(length(x1))
# # print(length(y1))
# # par(mar = c(1, 1, 1, 1))
# p3 <- ggplot(data, aes(x=year, y=clauses_per_sent)) +
#   geom_point() +
#   geom_smooth(method=lm , color="red", fill="#69b3a2", se=TRUE)

# p4 <- ggplot(data, aes(x=year, y=avg_aoa_min)) +
#   geom_point() +
#   geom_smooth(method=lm , color="red", fill="#69b3a2", se=TRUE)

# p5 <- ggplot(data, aes(x=year, y=avg_word_freq_stopless)) +
#   geom_point() +
#   geom_smooth(method=lm , color="red", fill="#69b3a2", se=TRUE)

# p6 <- ggplot(data, aes(x=year, y=max_dependency_distance)) +
#   geom_point() +
#   geom_smooth(method=lm , color="red", fill="#69b3a2", se=TRUE)


# grid.arrange(p3, p4, p5, p6, ncol=1)
# print(which(x == "num_words"))

# n <- length(graphs)
# nCol <- floor(sqrt(n))
# print(graphs[0])
# grid.arrange(myplots[0])
# grid.arrange(myplots[0])

do.call("grid.arrange", myplots)

# print(colnames(results))

# print(plot_data_column(results, "num_tokens"))

t <- ggplot(results, aes(x=year, y=results[,"num_tokens"])) +
        geom_point() +
        geom_smooth(method=lm , color="red", fill="#69b3a2", se=TRUE)

# print(t)