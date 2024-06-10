import openai
from config import apikey  #for my program i have created another file named config.py to store the API key

# Set the API key
openai.api_key = apikey #get your API key from OpenAi and paste here

response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Write an article for healthy lifestyle\n\nIn today's fast-paced world, it can be challenging to maintain a healthy lifestyle. With busy work schedules, hectic social lives, and constant temptations, it's easy to neglect our physical and mental well-being. However, committing to a healthy lifestyle is one of the most important things we can do for ourselves. It not only improves our overall health but also enhances our quality of life. In this article, we will discuss the benefits of a healthy lifestyle and provide some tips on how to achieve and maintain it.\n\nFirst and foremost, a healthy lifestyle includes maintaining a balanced and nutritious diet. It's essential to fuel our bodies with the right nutrients and vitamins to stay healthy and energized. This means incorporating a variety of fruits, vegetables, lean proteins, and whole grains into our daily meals. Avoiding processed and sugary foods can also help lower the risk of developing chronic diseases such as obesity, heart disease, and diabetes.\n\nIn addition to a healthy diet, regular exercise is crucial for a healthy lifestyle. Regular physical activity not only helps maintain a healthy weight but also has countless other benefits. It reduces the risk of developing chronic diseases, such as cardiovascular disease and certain types of cancer, and can also improve mental health by reducing stress and anxiety. Finding an exercise routine that",
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# Print the response
print(response.choices[0].text.strip())
