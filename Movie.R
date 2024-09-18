library(rvest)
library(dplyr)

url <- "https://www.imdb.com/chart/top/"

# Read the HTML content of the page
page <- read_html(url)

# titles
movie_titles <- page %>%
  html_nodes("h3.ipc-title__text") %>%
  html_text()
# Delete first index of titles 
movie_titles <- movie_titles[-c(1, 27)]

# years
movie_years <- page %>%
  html_nodes(".sc-b189961a-7.btCcOY.cli-title-metadata span:nth-child(1)") %>%
  html_text() %>%
  as.numeric()

# ratings
movie_ratings <- page %>%
  html_nodes(".ipc-rating-star--rating") %>%
  html_text() %>%
  as.numeric()

# movie runtimes and convert to total minutes
movie_runtimes <- page %>%
  html_nodes(".sc-b189961a-7.btCcOY.cli-title-metadata span:nth-child(2)") %>%
  html_text() %>%
  gsub("h", "h ", .) %>% # Add space after 'h'
  gsub("m", "m ", .) %>% # Add space after 'm'
  sapply(function(x) {
    time_parts <- strsplit(x, " ")[[1]] # Split by space
    hours <- ifelse(length(time_parts) > 0 && grepl("h", time_parts[1]), 
                    as.numeric(gsub("h", "", time_parts[1])), 0) # Get hours
    minutes <- ifelse(length(time_parts) > 1 && grepl("m", time_parts[2]), 
                      as.numeric(gsub("m", "", time_parts[2])), 0) # Get minutes
    return(hours * 60 + minutes) # Convert to total minutes
  })

# movie classifications (ratings)
movie_classifications <- page %>%
  html_nodes(".sc-b189961a-7.btCcOY.cli-title-metadata span:nth-child(3)") %>%
  html_text()

# Check lengths
lengths <- c(
  Titles = length(movie_titles),
  Years = length(movie_years),
  Ratings = length(movie_ratings),
  Runtimes = length(movie_runtimes),
  Classifications = length(movie_classifications)
)


# into a data frame if lengths match
movies_df <- data.frame(
  Title = movie_titles,
  Year = movie_years,
  Rating = movie_ratings,
  Runtime = movie_runtimes,
  Classification = movie_classifications
)

# Convert data frame to CSV
write.csv(movies_df, "movies.csv", row.names = FALSE)
