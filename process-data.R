library(tidyverse)

d <- read_csv("all-schools-2021-all-data.csv")

logs <- read_lines("logs/2022-11-08-log.txt")

logs <- logs %>% 
  as_tibble() %>% 
  filter(str_detect(value, "FAILED"))

logs$nces_name_plus_zipcode <- str_split(logs$value, "FAILED") %>% 
  map_chr(~.[[1]])

logs <- logs %>% 
  select(nces_name_plus_zipcode) %>% 
  mutate(rating = NA, n_reviews = NA)

d <- d %>% 
  janitor::clean_names()

d$nces_name_plus_zipcode <- str_c(d$school_name, " ", d$location_zip_public_school_2020_21)

out <- read_csv("output-for-all.csv")

out$nces_name_plus_zipcode <- str_c(out$nces_name, " ", out$zipcode)

out <- out %>% 
  select(nces_name_plus_zipcode, rating, n_reviews)

out <- out %>% 
  bind_rows(logs)

d <-d %>% 
  distinct(nces_name_plus_zipcode, .keep_all = TRUE)

all_data <- out %>% 
  left_join(d)

all_data <- all_data %>% 
  select(school_name, rating, n_reviews, everything())

write_csv(all_data, 'nc-schools-google-maps-with-nces-data.csv')
