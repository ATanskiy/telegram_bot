# tests/test_interactions_sync.py
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from Interactions import (
    get_motivational_quote, get_latest_movies, get_llm_model,
    start_command, help_command, datetime_command,
    text_response, get_quote, movies_command, llama2
)

class TestInteractionsSync(unittest.TestCase):

    @patch('Interactions.requests.get')
    def test_get_motivational_quote_success(self, mock_get):
        mock_get.return_value.json.return_value = [{'q': 'Stay strong', 'a': 'Someone'}]
        result = get_motivational_quote()
        self.assertEqual(result, 'Stay strong - Someone')

    @patch('Interactions.requests.get')
    def test_get_motivational_quote_empty(self, mock_get):
        mock_get.return_value.json.return_value = []
        with self.assertRaises(IndexError):
            get_motivational_quote()

    @patch('Interactions.requests.get')
    def test_get_latest_movies_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            'results': [{'title': 'Test Movie', 'release_date': '2025-01-01', 'overview': 'Test overview'}]
        }
        result = get_latest_movies()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Test Movie')

    @patch('Interactions.requests.get')
    def test_get_latest_movies_empty(self, mock_get):
        mock_get.return_value.json.return_value = {'results': []}
        result = get_latest_movies()
        self.assertEqual(result, [])

    def test_get_llm_model(self):
        result = get_llm_model()
        self.assertEqual(result, [1, 2, 3])


class TestInteractionsAsync(unittest.IsolatedAsyncioTestCase):

    async def test_start_command(self):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        await start_command(update, context)
        update.message.reply_text.assert_awaited_once()

    async def test_help_command(self):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        await help_command(update, context)
        update.message.reply_text.assert_awaited_once()

    async def test_datetime_command(self):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        await datetime_command(update, context)
        update.message.reply_text.assert_awaited_once()

    async def test_text_response_ping(self):
        update = MagicMock()
        update.message.text = 'ping'
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        await text_response(update, context)
        update.message.reply_text.assert_awaited_once_with("pong")

    async def test_text_response_meow(self):
        update = MagicMock()
        update.message.text = 'meow'
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        await text_response(update, context)
        update.message.reply_text.assert_awaited_once_with("meow")

    @patch('Interactions.get_motivational_quote', return_value="Test Quote - Author")
    async def test_get_quote_command(self, mock_quote):
        update = MagicMock()
        update.message.text = '/quote'
        update.message.from_user.id = 123
        update.message.chat_id = 123
        context = MagicMock()
        context.user_data = {}
        context.bot.id = 456
        context.bot.send_message = AsyncMock()
        await get_quote(update, context)
        context.bot.send_message.assert_awaited()

    @patch('Interactions.get_latest_movies')
    async def test_movies_command_success(self, mock_get_movies):
        mock_get_movies.return_value = [
            {'title': 'Mock Movie', 'release_date': '2025-01-01', 'overview': 'Great!'}
        ]
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        await movies_command(update, context)
        update.message.reply_text.assert_awaited()

    @patch('Interactions.replicate.run', return_value=["This is a test response."])
    async def test_llama2(self, mock_run):
        update = MagicMock()
        update.message.reply_text = AsyncMock()
        context = MagicMock()
        await llama2(update, context, "hi")
        update.message.reply_text.assert_awaited_once()
